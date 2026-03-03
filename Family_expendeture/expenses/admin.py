
from django.contrib import admin
from .models import ExpenseCategory, FamilyMember, Expenditure, Budget, SavingsGoal, ActivityLog

# নতুন মডেলগুলো রেজিস্টার করুন
admin.site.register(ExpenseCategory)
admin.site.register(FamilyMember)
admin.site.register(Expenditure)

# # আগের গুলো যদি অলরেডি রেজিস্টার করা না থাকে
# admin.site.register(Budget)
# admin.site.register(SavingsGoal)
# admin.site.register(ActivityLog)