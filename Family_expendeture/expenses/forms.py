from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, ExpenseCategory
from .models import Budget, FamilyMember


class ExpenseForm(forms.ModelForm):
    """খরচ ফর্ম"""

    class Meta:
        model = Expense
        fields = ["amount", "category", "description", "date"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "৳ 0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "খরচের বর্ণনা লিখুন",
                }
            ),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False
        self.fields["category"].queryset = ExpenseCategory.objects.all()
        self.fields["category"].empty_label = "-- Category Select করুন --"


class UserCreationFormCustom(UserCreationForm):
    """ব্যবহারকারী তৈরির ফর্ম"""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "ইমেইল ঠিকানা"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ইউজারনেম"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "পাসওয়ার্ড"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "পাসওয়ার্ড নিশ্চিত করুন"}
        )


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["monthly_budget"]
        widgets = {
            "monthly_budget": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter monthly budget in TK",
                    "step": "0.01",
                    "min": "0",
                }
            )
        }


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = [
            "name",
            "father_name",
            "phone_number",
            "income_source",
            "salary",
            "role",
            "photo",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "father_name": forms.TextInput(attrs={"class": "form-control"}),
            # এভাবেই অন্য ফিল্ডগুলোতে CSS ক্লাস যোগ করা যায়
        }
