from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    ExpenseViewSet,
    FamilyMemberViewSet,
    IncomeSourceViewSet,
    ExpenseCategoryViewSet,
    ExpenditureViewSet,
)

# ১. রাউটার কনফিগারেশন
router = DefaultRouter()
router.register(r"expenses-api", ExpenseViewSet, basename="expense-api")
router.register(r"members", FamilyMemberViewSet, basename="member")
router.register(r"income-sources", IncomeSourceViewSet, basename="income-source")
router.register(r"categories", ExpenseCategoryViewSet, basename="category")
router.register(r"expenditures", ExpenditureViewSet, basename="expenditure")

app_name = "expenses"

urlpatterns = [
    # ২. DRF API URLs
    path("api/", include(router.urls)),
    # ৩. আপনার বিদ্যমান HTML Template URLs
    path("", views.home, name="home"),
    path("add/", views.add_expense, name="add_expense"),
    path("view/", views.view_expenses, name="view_expenses"),
    path("edit/<int:pk>/", views.edit_expense, name="edit_expense"),
    path("delete/<int:pk>/", views.delete_expense, name="delete_expense"),
    path("stats/", views.expense_stats, name="stats"),
    path("budget/", views.set_budget, name="set_budget"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("members/add/", views.add_member, name="add_member"),
    path("members/", views.member_list, name="member_list"),
    path("categories/manage/", views.add_category, name="add_category"),
    path("categories/edit/<int:pk>/", views.edit_category, name="edit_category"),
    path("categories/delete/<int:pk>/", views.delete_category, name="delete_category"),
]
