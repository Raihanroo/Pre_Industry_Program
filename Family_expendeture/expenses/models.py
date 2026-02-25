from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("RELIGION ABAYA", "Religion Abaya"),
        ("GROCERIES", "Groceries"),
        ("UTILITIES", "Utilities"),
        ("ENTERTAINMENT", "Entertainment"),
        ("TRANSPORT", "Transport"),
        ("HEALTH", "Health"),
        ("EDUCATION", "Education"),
    ]

    FREQUENCY_CHOICES = [
        ("ONCE", "One Time"),
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # নতুন ফিল্ড - রিকারিং খরচের জন্য
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
    # এখানে default=0.00 যোগ করা হয়েছে
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # নতুন ফিল্ড - সতর্কতা সীমা
    alert_percentage = models.IntegerField(
        default=80, help_text="বাজেটের কত % খরচ হলে সতর্কতা দেবে"
    )

    def __str__(self):
        return f"{self.user.username} - {self.monthly_budget} টাকা"


class SavingsGoal(models.Model):
    """সঞ্চয় লক্ষ্য ট্র্যাকিং এর জন্য"""

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
        """সঞ্চয়ের শতাংশ বের করুন"""
        if self.target_amount > 0:
            return int((self.current_amount / self.target_amount) * 100)
        return 0


class ActivityLog(models.Model):
    """সকল কার্যকলাপের লগ রাখুন (অডিট ট্রেইল)"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_logs"
    )
    action = models.CharField(max_length=200)  # "Created", "Updated", "Deleted"
    model_name = models.CharField(max_length=100)  # "Expense", "Budget"
    object_id = models.IntegerField(null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.username} - {self.action} {self.model_name}"


class FamilyMember(models.Model):
    """পরিবারের সদস্য এবং শেয়ারিং এর জন্য"""

    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
        ("VIEWER", "Viewer"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="family_memberships"
    )
    family_head = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="family_members"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="MEMBER")
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "family_head")

    def __str__(self):
        return (
            f"{self.user.username} - {self.family_head.username}'s family ({self.role})"
        )
