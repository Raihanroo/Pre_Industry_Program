# forms.py

from django import forms
from .models import UserMessage

class MessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['name', 'email', 'message']
    
    # কাস্টম এরর মেসেজ (বাংলায় বা ইংরেজিতে যা চাও)
    error_messages = {
        'email': {
            'invalid': 'একটি সঠিক ইমেইল ঠিকানা দিন। (উদাহরণ: example@gmail.com)',
            # অথবা ইংরেজিতে: 'Enter a valid email address.'
        }
    }