from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.db.models import Sum
from django.http import JsonResponse
import json

# ১. মেইন ড্যাশবোর্ড (লগইন করা থাকলে দেখা যাবে)
@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_spending = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    context = {
        'expenses': expenses,
        'total_spending': total_spending,
        'username': request.user.username
    }
    return render(request, 'expenses/home.html', context)

# ২. রেজিস্ট্রেশন ভিউ
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'expenses/register.html', {'form': form})

# ৩. লগইন ভিউ
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'expenses/login.html', {'form': form})

# ৪. লগআউট ভিউ
def logout_view(request):
    logout(request)
    return redirect('login')

# ৫. খরচ ডিলিট করার API
@login_required
def delete_expense_api(request, expense_id):
    if request.method == 'POST':
        try:
            expense = Expense.objects.get(id=expense_id, user=request.user)
            expense.delete()
            return JsonResponse({'success': True, 'message': 'Deleted successfully'})
        except Expense.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Expense not found'})

# ৬. খরচ আপডেট করার API (আপনার Edit চাহিদার জন্য)
@login_required
def update_expense_api(request, expense_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            expense = Expense.objects.get(id=expense_id, user=request.user)
            expense.category = data.get('category', expense.category)
            expense.description = data.get('description', expense.description)
            expense.amount = data.get('amount', expense.amount)
            expense.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

# ৭. নতুন খরচ যোগ করার API
@login_required
def add_expense_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Expense.objects.create(
                user=request.user,
                date=data.get('date'),
                category=data.get('category'),
                description=data.get('description'),
                amount=data.get('amount')
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})