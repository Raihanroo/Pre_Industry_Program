from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    # User Profile (Username, Email, Password handles by Django's User model)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # খরচ
    category = models.CharField(max_length=100)  # ক্যাটাগরি
    description = models.TextField(blank=True)  # বর্ণনা
    date = models.DateField(auto_now_add=True)  # সময়

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
# views.py
expenses = Expense.objects.all().order_by('-date')
description = models.CharField(max_length=500, blank=True, null=True)