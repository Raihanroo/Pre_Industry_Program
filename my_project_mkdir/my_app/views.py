from django.shortcuts import render
from .forms import MessageForm

def contact_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save() # এটি ডাটাবেসে সেভ করবে
            return render(request, 'contact.html', {'form': MessageForm(), 'success': True})
    else:
        form = MessageForm()
    
    return render(request, 'contact.html', {'form': form})