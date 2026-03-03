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
# নিচে এই দুটি লাইন নতুন যোগ করুন
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API এবং সাধারণ ভিউ সব এই এক লাইনেই ইনক্লুড হবে
    path('expenses/', include('expenses.urls')), 
    
    # ইউজার যদি শুধু মেইন ডোমেইনে আসে, তবে তাকে লগইনে পাঠিয়ে দেবে
    path('', RedirectView.as_view(url='/expenses/login/', permanent=False)),

]

# এটি যোগ করুন যাতে ডেভেলপমেন্ট মোডে আপলোড করা ছবি দেখা যায়
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)