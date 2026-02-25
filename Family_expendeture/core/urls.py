"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('api-auth/', include('rest_framework.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # নিশ্চিত করুন namespace="expenses" ঠিকমতো দেওয়া আছে
    path('expenses/', include('expenses.urls', namespace='expenses')), 
    # হোম পেজে গেলে সরাসরি লগইন বা ড্যাশবোর্ডে পাঠানোর জন্য
    path('', RedirectView.as_view(url='/expenses/login/', permanent=False)),
]