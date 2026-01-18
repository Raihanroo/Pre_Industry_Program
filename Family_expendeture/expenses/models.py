
from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('RELIGION ABAYA', 'Religion Abaya'),
        ('GROCERIES', 'Groceries'),
        ('UTILITIES', 'Utilities'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('TRANSPORT', 'Transport'),
        ('HEALTH', 'Health'),
        ('EDUCATION', 'Education'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # ৳10000.00 পর্যন্ত
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)  # খরচের বর্ণনা
    date = models.DateField()  # খরচের তারিখ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount} TK"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Expenses"