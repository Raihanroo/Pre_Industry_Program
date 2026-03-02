from rest_framework import serializers
from .models import Expense  # আপনার মডেলের নাম অনুযায়ী (ধরে নিলাম Expense)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"  # আপনি চাইলে নির্দিষ্ট ফিল্ডও দিতে পারেন
