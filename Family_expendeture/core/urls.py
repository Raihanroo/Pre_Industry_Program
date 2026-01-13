"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from expenses import views as expense_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls), # অ্যাডমিন প্যানেল
    path('register/', expense_views.register, name='register'), # রেজিস্ট্রেশন পেজ
    path('login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'), # লগইন
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # লগআউট
    path('', expense_views.home, name='home'), # মেইন ড্যাশবোর্ড
    path('add-expense/', expense_views.add_expense, name='add_expense'), # খরচ যোগ করার পেজ
]