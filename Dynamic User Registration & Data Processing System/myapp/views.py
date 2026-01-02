from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def register(request):
    if request.method == "POST":
        # to recive data from the form
        name  = request.POST.get("name")
        email = request.POST.get("email")
        # base on my proposal HttpResponse to show the data
        return HttpResponse(
            f"<h1>Success!</h1><p>Name: {name}</p><p>Email: {email}</p>"
        )

    # you will inside the first page this form
    return render(request, "register.html")
