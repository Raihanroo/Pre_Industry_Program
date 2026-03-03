from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from .models import Expense, Budget
from .forms import BudgetForm, ExpenseForm
from django.contrib.auth.models import User
import json
from rest_framework import viewsets, permissions  # permissions যোগ করা হয়েছে
from .models import (
    Expense,
    Budget,
    FamilyMember,
    IncomeSource,
    ExpenseCategory,
    Expenditure,
)
from .serializers import (
    ExpenseSerializer,
    FamilyMemberSerializer,
    IncomeSourceSerializer,
    ExpenseCategorySerializer,
    ExpenditureSerializer,
)


class IncomeSourceViewSet(viewsets.ModelViewSet):
    # আয়ের উৎস এর CRUD operations
    queryset = IncomeSource.objects.all()
    serializer_class = IncomeSourceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    # Expenditure Category এর CRUD operations
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class FamilyMemberViewSet(viewsets.ModelViewSet):
    # Family Member এর CRUD operations
    queryset = FamilyMember.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenditureViewSet(viewsets.ModelViewSet):
    # Expenditure এর CRUD operations
    queryset = Expenditure.objects.all()
    serializer_class = ExpenditureSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    # এটি নিশ্চিত করবে যে শুধু লগইন করা ইউজাররা API ব্যবহার করতে পারবে
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # এটি নিশ্চিত করবে যে একজন ইউজার শুধু নিজের ডেটাই দেখতে/এডিট করতে পারবে
        return Expense.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        # নতুন খরচ সেভ করার সময় অটোমেটিক বর্তমান ইউজারকে অ্যাসাইন করবে
        serializer.save(user=self.request.user)


# Home/Dashboard View
@login_required
def home(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by("-date")

    # Current month expenses
    today = datetime.today()
    current_month_expenses = expenses.filter(
        date__year=today.year, date__month=today.month
    )

    # Last 7 days expenses
    last_7_days = datetime.today() - timedelta(days=7)
    last_7_expenses = expenses.filter(date__gte=last_7_days)

    # Group by date for chart
    daily_expenses = (
        last_7_expenses.values("date").annotate(total=Sum("amount")).order_by("date")
    )

    # Total amount this month
    total_this_month = (
        current_month_expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    )

    # Total amount all time
    total_all_time = expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    # Category-wise breakdown (this month)
    category_breakdown = (
        current_month_expenses.values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    # Prepare data for charts
    pie_labels = []
    pie_data = []
    # এটি চার্টের জন্য লেবেল সেট করবে
    category_dict = {cat.id: cat.name for cat in ExpenseCategory.objects.all()}
    for item in category_breakdown:
        # item["category"] যদি ID হয়, তবে নাম খুঁজে বের করবে
        cat_name = category_dict.get(item["category"], "Unknown")
        pie_labels.append(cat_name)
        pie_data.append(float(item["total"]))

    bar_labels = []
    bar_data = []
    for item in daily_expenses:
        bar_labels.append(item["date"].strftime("%d %b"))
        bar_data.append(float(item["total"]))

    context = {
        "expenses": expenses[:10],
        "total_this_month": total_this_month,
        "total_all_time": total_all_time,
        "category_breakdown": category_breakdown,
        "total_expenses_count": expenses.count(),
        "pie_labels": json.dumps(pie_labels),
        "pie_data": json.dumps(pie_data),
        "bar_labels": json.dumps(bar_labels),
        "bar_data": json.dumps(bar_data),
    }
    return render(request, "expenses/home.html", context)


# Add Expense View
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

    context = {"form": form}
    return render(request, "expenses/add_expense.html", context)


# View All Expenses
@login_required
def view_expenses(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by("-date")

    category = request.GET.get("category")
    if category:
        expenses = expenses.filter(category=category)

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if from_date:
        expenses = expenses.filter(date__gte=from_date)
    if to_date:
        expenses = expenses.filter(date__lte=to_date)

    total_amount = expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    context = {
        "expenses": expenses,
        "categories": ExpenseCategory.objects.all(),
        "total_amount": total_amount,
    }
    return render(request, "expenses/view_expenses.html", context)


# Edit Expense View
@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect("expenses:view_expenses")
    else:
        form = ExpenseForm(instance=expense)

    context = {
        "form": form,
        "expense": expense,
        "is_edit": True,
    }
    return render(request, "expenses/add_expense.html", context)


# Delete Expense View
@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect("expenses:view_expenses")

    context = {"expense": expense}
    return render(request, "expenses/confirm_delete.html", context)


# Add Member - HTML Form View
@login_required
def add_member(request):
    if request.method == "POST":
        # Form data নেওয়া
        user_id = request.POST.get("user")
        role = request.POST.get("role")
        name = request.POST.get("name")
        father_name = request.POST.get("father_name")
        mother_name = request.POST.get("mother_name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        income_source = request.POST.get("income_source")
        salary = request.POST.get("salary")

        # Member save করা
        FamilyMember.objects.create(
            user_id=user_id,
            role=role,
            name=name,
            father_name=father_name,
            mother_name=mother_name,
            phone_number=phone_number,
            address=address,
            income_source=income_source if income_source else None,
            salary=salary if salary else None,
        )
        messages.success(request, "Member added successfully!")
        return redirect("expenses:member_list")

    # GET request — form দেখাও
    users = User.objects.all()
    context = {
        "users": users,
        "roles": FamilyMember.ROLE_CHOICES,
    }
    return render(request, "expenses/add_member.html", context)


# Member List View
@login_required
def member_list(request):
    members = FamilyMember.objects.all()
    context = {"members": members}
    return render(request, "expenses/member_list.html", context)


# add category
@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        ExpenseCategory.objects.create(name=name)
        messages.success(request, "Category added successfully!")
        return redirect("expenses:add_category")

    categories = ExpenseCategory.objects.all()
    context = {"categories": categories}
    return render(request, "expenses/add_category.html", context)


# edit_category
@login_required
def edit_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        messages.success(request, "Category updated!")
        return redirect("expenses:add_category")
    context = {"category": category}
    return render(request, "expenses/edit_category.html", context)


# delete_category
@login_required
def delete_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    category.delete()
    messages.success(request, "Category deleted!")
    return redirect("expenses:add_category")


# Expense Statistics
@login_required
def expense_stats(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)

    last_30_days = datetime.today() - timedelta(days=30)
    last_30_expenses = expenses.filter(date__gte=last_30_days)
    total_last_30 = last_30_expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    category_stats = (
        expenses.values("category")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )

    context = {
        "total_last_30": total_last_30,
        "category_stats": category_stats,
    }
    return render(request, "expenses/stats.html", context)


# Authentication Views
# Authentication Views
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match!")
            return redirect("expenses:register")  # Added namespace

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("expenses:register")  # Added namespace

        # Create user
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        # This was the line causing the error:
        return redirect("expenses:login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("expenses:home")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("expenses:login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("expenses:login")


# Set Budget View
@login_required
def set_budget(request):
    user = request.user
    budget, created = Budget.objects.get_or_create(user=user)

    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully!")
            return redirect("expenses:home")
    else:
        form = BudgetForm(instance=budget)

    context = {"form": form, "budget": budget}
    return render(request, "expenses/set_budget.html", context)


# Get Budget Info (helper function – no change needed)
def get_budget_info(user):
    try:
        budget = Budget.objects.get(user=user)
        today = datetime.today()
        current_month_expenses = (
            Expense.objects.filter(
                user=user, date__year=today.year, date__month=today.month
            ).aggregate(Sum("amount"))["amount__sum"]
            or 0
        )

        remaining = budget.monthly_budget - current_month_expenses
        percentage = (
            (current_month_expenses / budget.monthly_budget * 100)
            if budget.monthly_budget > 0
            else 0
        )

        return {
            "budget": budget.monthly_budget,
            "spent": current_month_expenses,
            "remaining": remaining,
            "percentage": percentage,
            "exceeded": remaining < 0,
        }
    except Budget.DoesNotExist:
        return None
