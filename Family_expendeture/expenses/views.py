from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum

# ১. মেম্বার রেজিস্ট্রেশন
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "expenses/register.html", {"form": form})

# ২. হোম পেজ বা ড্যাশবোর্ড (Updated & Cleaned)
@login_required # Login chara dashboard dekha jabe na
def home(request):
    # Shudhu matro login kora user-er data ashbe
    expenses = Expense.objects.filter(user=request.user).order_by("-date") # -timestamp bad diye -date use kora hoyeche
    
    # Database theke total amount calculate kora
    total_amount = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    
    context = {
        "expenses": expenses,
        "total_amount": total_amount
    }
    return render(request, "expenses/home.html", context)

# ৩. নতুন খরচ যোগ করা
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user # User set kora hochche jate kar khoroch sheta bojha jay
            expense.save()
            return redirect("home")
    else:
        form = ExpenseForm()
    return render(request, "expenses/add_expense.html", {"form": form})
