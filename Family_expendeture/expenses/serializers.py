from rest_framework import serializers

# DRF (Django REST Framework) থেকে serializers import করছি
# serializers হলো Database data কে JSON এ convert করার tool

from .models import FamilyMember, IncomeSource, MemberCategory, Expenditure, Expense

# আমাদের বানানো 4টা model import করছি


class IncomeSourceSerializer(serializers.ModelSerializer):
    # IncomeSource model এর জন্য serializer
    # যেমন: {"id": 1, "name": "চাকরি"} এই format এ data আসবে
    class Meta:
        model = IncomeSource  # কোন model এর জন্য
        fields = "__all__"  # সব field JSON এ আসবে


class MemberCategorySerializer(serializers.ModelSerializer):
    # MemberCategory model এর জন্য serializer
    # যেমন: {"id": 1, "name": "খাবার"} এই format এ data আসবে
    class Meta:
        model = MemberCategory  # কোন model এর জন্য
        fields = "__all__"  # সব field JSON এ আসবে


class FamilyMemberSerializer(serializers.ModelSerializer):
    # FamilyMember model এর জন্য serializer

    income_source_name = serializers.CharField(
        source="income_source.name",
        read_only=True,
        # source='income_source.name' মানে: ForeignKey দিয়ে গিয়ে IncomeSource এর name নিয়ে আসো
        # read_only=True মানে: শুধু দেখা যাবে, পরিবর্তন করা যাবে না
    )

    class Meta:
        model = FamilyMember
        fields = [
            "id",  # Member এর unique ID
            "user",  # কোন User এর সাথে linked
            "family_head",  # পরিবারের প্রধান কে
            "role",  # ADMIN / MEMBER / VIEWER
            "joined_date",  # কবে যোগ দিয়েছে
            "name",  # Member এর নাম
            "father_name",  # বাবার নাম
            "mother_name",  # মায়ের নাম
            "phone_number",  # ফোন নম্বর
            "address",  # ঠিকানা
            "income_source",  # আয়ের উৎস এর ID আসবে
            "income_source_name",  # আয়ের উৎস এর নাম আসবে (যেমন: "চাকরি")
            "salary",  # মাসিক বেতন/আয়
        ]


class ExpenditureSerializer(serializers.ModelSerializer):
    # Expenditure model এর জন্য serializer

    member_name = serializers.CharField(
        source="member.name",
        read_only=True,
        # Member এর ID না, নাম দেখাবে (যেমন: "রাইহান")
    )
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
        # Category এর ID না, নাম দেখাবে (যেমন: "খাবার")
    )

    class Meta:
        model = Expenditure
        fields = [
            "id",  # Expenditure এর unique ID
            "member",  # Member এর ID
            "member_name",  # Member এর নাম (যেমন: "রাইহান")
            "category",  # Category এর ID
            "category_name",  # Category এর নাম (যেমন: "খাবার")
            "amount",  # কত টাকা খরচ হয়েছে
            "description",  # খরচের বিবরণ
            "date",  # কোন তারিখে খরচ হয়েছে
            "created_at",  # কখন record করা হয়েছে
        ]


class ExpenseSerializer(serializers.ModelSerializer):
    # Expense model এর জন্য serializer
    class Meta:
        model = Expense
        fields = "__all__"
