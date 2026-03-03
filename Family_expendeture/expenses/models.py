from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Expense(models.Model):
    # ... your other fields (amount, date, etc.)
    FREQUENCY_CHOICES = [
        ("ONCE", "One Time"),
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        "ExpenseCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_recurring = models.BooleanField(default=False)
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, null=True, blank=True
    )
    recurring_end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount} টাকা"


class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="budget")
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alert_percentage = models.IntegerField(
        default=80, help_text="বাজেটের কত % খরচ হলে সতর্কতা দেবে"
    )

    def __str__(self):
        return f"{self.user.username} - {self.monthly_budget} টাকা"


class SavingsGoal(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="savings_goals"
    )
    goal_name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-deadline"]

    def __str__(self):
        return f"{self.user.username} - {self.goal_name}"

    def get_percentage(self):
        if self.target_amount > 0:
            return int((self.current_amount / self.target_amount) * 100)
        return 0


class ActivityLog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_logs"
    )
    action = models.CharField(max_length=200)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username} - {self.action} {self.model_name}"


# ✅ নতুন — আয়ের উৎস
class IncomeSource(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ নতুন — Expenditure Category
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ আপডেট — FamilyMember
class FamilyMember(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
        ("Visitor", "Visitor"),
    ]
    photo = models.ImageField(upload_to="member_photos/", null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="family_memberships"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="MEMBER")
    joined_date = models.DateTimeField(auto_now_add=True)

    # ✅ নতুন fields
    name = models.CharField(max_length=100, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    income_source = models.ForeignKey(
        IncomeSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name or self.user.username} - {self.role}"


# ✅ নতুন — Expenditure
class Expenditure(models.Model):
    member = models.ForeignKey(
        FamilyMember, on_delete=models.CASCADE, related_name="expenditures"
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="expenditures",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.name} → {self.category} → {self.amount}৳"
