from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
import pandas as pd
import json
import xlwt
from django.http import HttpResponse

# REST Framework
from rest_framework import viewsets, permissions

# মডেল এবং ফর্ম ইম্পোর্ট
from .models import (
    Expense,
    Budget,
    FamilyMember,
    IncomeSource,
    ExpenseCategory,
    Expenditure,
)
from .forms import BudgetForm, ExpenseForm, FamilyMemberForm
from .serializers import (
    ExpenseSerializer,
    FamilyMemberSerializer,
    IncomeSourceSerializer,
    ExpenseCategorySerializer,
    ExpenditureSerializer,
)


# --- API ViewSets ---
class IncomeSourceViewSet(viewsets.ModelViewSet):
    queryset = IncomeSource.objects.all()
    serializer_class = IncomeSourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class FamilyMemberViewSet(viewsets.ModelViewSet):
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenditureViewSet(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all()
    serializer_class = ExpenditureSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- Dashboard View ---
@login_required
def home(request):
    user = request.user
    search_query = request.GET.get("search", "").strip()
    all_expenses = (
        Expense.objects.filter(user=user)
        .select_related("category", "member__user")
        .order_by("-date")
    )

    # --- সার্চ লজিক ---
    converted_date = None
    if search_query:
        for fmt in ("%d %b, %Y", "%d %b %Y", "%Y-%m-%d"):
            try:
                converted_date = datetime.strptime(search_query, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue

    if search_query:
        query_filter = (
            Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
            | Q(member__name__icontains=search_query)
            | Q(member__user__username__icontains=search_query)
        )
        if converted_date:
            query_filter |= Q(date=converted_date)
        expenses = all_expenses.filter(query_filter).distinct()
    else:
        expenses = all_expenses[:10]

    # --- স্ট্যাটাস ক্যালকুলেশন ---
    today = datetime.today()
    current_month_expenses = all_expenses.filter(
        date__year=today.year, date__month=today.month
    )
    total_this_month = current_month_expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    total_all_time = all_expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    # --- Pie Chart ডেটা ---
    category_breakdown = (
        current_month_expenses.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    pie_labels = [item["category__name"] or "General" for item in category_breakdown]
    pie_data = [float(item["total"]) for item in category_breakdown]

    # --- Bar Chart ডেটা (আপনার নতুন যোগ করা অংশ) ---
    seven_days_ago = today - timedelta(days=7)
    last_7_days_expenses = all_expenses.filter(date__gte=seven_days_ago)
    daily_spending = (
        last_7_days_expenses.values("date")
        .annotate(total=Sum("amount"))
        .order_by("date")
    )
    bar_labels = [item["date"].strftime("%d %b") for item in daily_spending]
    bar_data = [float(item["total"]) for item in daily_spending]

    # --- ফাইনাল কনটেক্সট (সব ডেটা একসাথে) ---
    context = {
        "expenses": expenses,
        "total_this_month": total_this_month,
        "total_all_time": total_all_time,
        "total_expenses_count": all_expenses.count(),
        "pie_labels": json.dumps(pie_labels),
        "pie_data": json.dumps(pie_data),
        "bar_labels": json.dumps(bar_labels),  # নতুন ডেটা
        "bar_data": json.dumps(bar_data),      # নতুন ডেটা
    }
    
    return render(request, "expenses/home.html", context)

# --- Export Excel ---
@login_required
def export_expenses_excel(request):
    search_query = request.GET.get("search", "").strip()
    expenses = (
        Expense.objects.filter(user=request.user)
        .select_related("category", "member")
        .order_by("-date")
    )

    if search_query:
        query_filter = (
            Q(description__icontains=search_query)
            | Q(category__name__icontains=search_query)
            | Q(member__name__icontains=search_query)
            | Q(member__user__username__icontains=search_query)
        )
        expenses = expenses.filter(query_filter).distinct()

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        f'attachment; filename="Report_{datetime.now().strftime("%Y-%m-%d")}.xls"'
    )
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Expenses")
    columns = ["Date", "Category", "Member", "Description", "Amount"]

    header_style = xlwt.XFStyle()
    header_style.font.bold = True
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, header_style)

    for row_num, obj in enumerate(expenses, 1):
        ws.write(row_num, 0, obj.date.strftime("%d %b, %Y"))
        ws.write(row_num, 1, obj.category.name if obj.category else "General")
        ws.write(row_num, 2, obj.member.name if obj.member else "Self")
        ws.write(row_num, 3, obj.description)
        ws.write(row_num, 4, float(obj.amount))

    wb.save(response)
    return response


# --- CRUD Operations ---
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect("expenses:home")
    else:
        form = ExpenseForm()
    return render(request, "expenses/add_expense.html", {"form": form})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect("expenses:home")
    else:
        form = ExpenseForm(instance=expense)
    return render(
        request, "expenses/add_expense.html", {"form": form, "edit_mode": True}
    )


@login_required
def delete_expense(request, pk):
    get_object_or_404(Expense, pk=pk, user=request.user).delete()
    messages.success(request, "Expense deleted!")
    return redirect("expenses:home")


# --- Category Management (এটি আপনার এররটি ঠিক করবে) ---
@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        ExpenseCategory.objects.create(name=name)
        messages.success(request, "Category added!")
        return redirect("expenses:add_category")
    return render(
        request,
        "expenses/add_category.html",
        {"categories": ExpenseCategory.objects.all()},
    )


@login_required
def edit_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        messages.success(request, "Category updated!")
        return redirect("expenses:add_category")
    return render(request, "expenses/edit_category.html", {"category": category})


@login_required
def delete_category(request, pk):
    get_object_or_404(ExpenseCategory, pk=pk).delete()
    return redirect("expenses:add_category")


# --- Member Management ---
@login_required
def add_member(request):
    # আপনার মডেল থেকে রোলের অপশনগুলো নিয়ে আসা
    roles = FamilyMember.ROLE_CHOICES  # আপনার মডেলে যদি ROLE_CHOICES থাকে

    if request.method == "POST":
        form = FamilyMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            messages.success(request, "Member added successfully!")
            return redirect("expenses:member_list")
    else:
        form = FamilyMemberForm()

    # context-এ roles অবশ্যই পাঠাতে হবে
    return render(
        request,
        "expenses/add_member.html",
        {"form": form, "roles": roles},  # contex এই লাইনটি আপনার আগে ছিল না
    )


@login_required
def member_list(request):
    query = request.GET.get("q", "")
    members = FamilyMember.objects.filter(user=request.user)

    if query:
        members = members.filter(name__icontains=query)

    # এক্সেল এক্সপোর্ট লজিক
    if request.GET.get("export") == "1":
        data = [
            {
                "Name": m.name,
                "Phone": m.phone_number,
                "Role": m.role,
                "Income Source": m.income_source,
                "Salary": m.salary,
            }
            for m in members
        ]
        df = pd.DataFrame(data)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=members.xlsx"
        df.to_excel(response, index=False)
        return response

    return render(request, "expenses/member_list.html", {"members": members})


# 'member_id' এর বদলে 'pk' লিখুন
@login_required
def edit_member(request, pk):
    # এখানেও member_id এর বদলে pk লিখুন
    member = get_object_or_404(FamilyMember, id=pk)

    roles = FamilyMember.ROLE_CHOICES

    if request.method == "POST":
        form = FamilyMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Member updated successfully!")
            return redirect("expenses:member_list")
    else:
        form = FamilyMemberForm(instance=member)

    return render(
        request,
        "expenses/add_member.html",
        {"form": form, "member": member, "edit_mode": True, "roles": roles},
    )


@login_required
def delete_member(request, pk):
    get_object_or_404(FamilyMember, id=pk, user=request.user).delete()
    return redirect("expenses:member_list")


# --- Authentication & Others ---
def register_view(request):
    if request.method == "POST":
        u, e, p1, p2 = (
            request.POST.get("username"),
            request.POST.get("email"),
            request.POST.get("password"),
            request.POST.get("password_confirm"),
        )
        if p1 == p2 and not User.objects.filter(username=u).exists():
            user = User.objects.create_user(username=u, email=e, password=p1)
            user.is_staff = user.is_superuser = True
            user.save()
            return redirect("expenses:login")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        u, p = request.POST.get("username"), request.POST.get("password")
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect("expenses:home")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("expenses:login")


@login_required
def set_budget(request):
    budget, _ = Budget.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect("expenses:home")
    return render(
        request, "expenses/set_budget.html", {"form": BudgetForm(instance=budget)}
    )


@login_required
def view_expenses(request):
    # ১. সব খরচ এবং ক্যাটাগরি নিয়ে আসা (লগইন করা ইউজারের জন্য)
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    categories = ExpenseCategory.objects.all()

    # ২. ফিল্টারিং লজিক (URL থেকে ডাটা নেওয়া)
    category_id = request.GET.get("category")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    # ফিল্টার অ্যাপ্লাই করা (এখানে ডাবল আন্ডারস্কোর __ ব্যবহার করা হয়েছে)
    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if from_date:
        expenses = expenses.filter(date__gte=from_date)
    if to_date:
        expenses = expenses.filter(date__lte=to_date)

    # ৩. এক্সেল এক্সপোর্ট লজিক (যদি ইউজার ডাউনলোড বাটনে ক্লিক করে)
    if request.GET.get("export") == "1":
        data = [
            {
                "Date": e.date.strftime("%d %b, %Y"),
                "Category": e.category.name if e.category else "General",
                "Description": e.description,
                "Amount": float(e.amount),
            }
            for e in expenses
        ]

        df = pd.DataFrame(data)
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=filtered_expenses.xlsx"

        # এক্সেল ফাইল তৈরি
        df.to_excel(response, index=False)
        return response

    # ৪. টোটাল হিসাব করা
    total_amount = expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    # ৫. টেমপ্লেটে ডাটা পাঠানো
    return render(
        request,
        "expenses/view_expenses.html",
        {"expenses": expenses, "categories": categories, "total_amount": total_amount},
    )


@login_required
def expense_stats(request):
    today = datetime.today()
    monthly_expenses = Expense.objects.filter(
        user=request.user, date__year=today.year, date__month=today.month
    )
    category_summary = (
        monthly_expenses.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    context = {
        "labels": json.dumps(
            [item["category__name"] or "General" for item in category_summary]
        ),
        "data": json.dumps([float(item["total"]) for item in category_summary]),
        "category_summary": category_summary,
        "current_month": today.strftime("%B %Y"),
    }
    return render(request, "expenses/stats.html", context)
