from django.urls import path
from . import views

urlpatterns = [
    # রুট ইউআরএল সরাসরি লগইনে পাঠাবে
    path('', views.login_view, name='login_redirect'), 
    
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('home/', views.home, name='home'), 
    
    # API endpoints
    path('api/expenses/add/', views.add_expense_api, name='add_expense'),
    path('api/expenses/update/<int:expense_id>/', views.update_expense_api, name='update_expense'),
    path('api/expenses/delete/<int:expense_id>/', views.delete_expense_api, name='delete_expense'),
]