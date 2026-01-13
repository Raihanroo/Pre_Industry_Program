from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")  # লিস্টে এগুলো দেখাবে
    list_filter = ("created_at",)  # তারিখ অনুযায়ী ফিল্টার
    search_fields = ("name", "email", "message")  # সার্চ করতে পারবে
    readonly_fields = ("created_at",)  # created_at এডিট করা যাবে না
