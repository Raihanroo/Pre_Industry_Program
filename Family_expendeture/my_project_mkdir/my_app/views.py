from django.shortcuts import render
from .models import Message           # তোমার মডেল ইমপোর্ট করো
from django import forms

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your message',
            }),
        }

def contact_view(request):
    success = False
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()               # এখানে save() কাজ করবে
            success = True
            form = MessageForm()      # নতুন খালি ফর্ম দেখানোর জন্য
    else:
        form = MessageForm()

    return render(request, 'contact.html', {
        'form': form,
        'success': success
    })