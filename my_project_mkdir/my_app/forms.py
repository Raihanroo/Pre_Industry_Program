from django import forms
from .models import UserMessage

class MessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['name', 'email', 'message']