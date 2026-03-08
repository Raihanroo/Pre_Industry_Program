from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, ExpenseCategory, Budget, FamilyMember


class ExpenseForm(forms.ModelForm):
    """খরচ ফর্ম"""

    class Meta:
        model = Expense
        # এখানে member, is_recurring, frequency, recurring_end_date যোগ করা হয়েছে
        fields = [
            "date",
            "category",
            "member",
            "amount",
            "description",
            "is_recurring",
            "frequency",
            "recurring_end_date",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "member": forms.Select(
                attrs={"class": "form-control"}
            ),  # নতুন যোগ করা হয়েছে
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "৳ 0.00",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "খরচের বর্ণনা লিখুন",
                }
            ),
            # রিকারিং খরচের জন্য নতুন উইজেট
            "is_recurring": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "frequency": forms.Select(attrs={"class": "form-control"}),
            "recurring_end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False
        self.fields["category"].queryset = ExpenseCategory.objects.all()
        self.fields["category"].empty_label = "-- Category Select করুন --"

        # মেম্বার ড্রপডাউন সেটআপ
        self.fields["member"].queryset = FamilyMember.objects.all()
        self.fields["member"].empty_label = "-- মেম্বার সিলেক্ট করুন --"

        # রিকারিং অপশনগুলো শুরুতে বাধ্যতামূলক নয়
        self.fields["frequency"].required = False
        self.fields["recurring_end_date"].required = False


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
        # এখানে 'mother_name' এবং 'address' যোগ করা হয়েছে
        fields = [
            "name",
            "father_name",
            "mother_name",  # নতুন যুক্ত
            "phone_number",
            "income_source",
            "salary",
            "address",      # নতুন যুক্ত
            "role",
            "photo",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "মেম্বারের পূর্ণ নাম"}
            ),
            "father_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "বাবার নাম"}
            ),
            "mother_name": forms.TextInput( # নতুন যুক্ত
                attrs={"class": "form-control", "placeholder": "মায়ের নাম"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ফোন নম্বর"}
            ),
            "income_source": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "আয়ের উৎস"}
            ),
            "salary": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "মাসিক আয়"}
            ),
            "address": forms.Textarea(      # নতুন যুক্ত
                attrs={"class": "form-control", "placeholder": "সম্পূর্ণ ঠিকানা", "rows": 3}
            ),
            "role": forms.Select(attrs={"class": "form-control"}),
        }
