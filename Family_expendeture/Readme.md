👨‍👩‍👧‍👦 Family Expenditure Tracker - Complete Project Guide
📋 Project Overview
Family Expenditure Tracker একটি Django ভিত্তিক ওয়েব application যা পরিবারের সকল খরচ ট্র্যাক করতে সাহায্য করে। এটি আপনাকে আপনার সমস্ত expense (খরচ) একটি নিরাপদ জায়গায় সংরক্ষণ করতে এবং analytics দেখতে দেয়।

🎯 এই App টা কী করে?
সহজ কথায়:
<img width="1683" height="768" alt="image" src="https://github.com/user-attachments/assets/b1d44749-d07c-4a9b-8066-54b60bf5685c" />
<img width="1874" height="869" alt="image" src="https://github.com/user-attachments/assets/12d5e949-81e8-4420-b3d0-3ae0c73b5782" />
<img width="1919" height="676" alt="image" src="https://github.com/user-attachments/assets/11e2d03c-9688-4f3b-932b-3331fe16e42a" />
<img width="1609" height="862" alt="image" src="https://github.com/user-attachments/assets/2dd11b2b-62e7-4f1f-a428-403b667e52e8" />
<img width="1836" height="720" alt="image" src="https://github.com/user-attachments/assets/061f7f7a-cb97-4a49-a496-785217397c57" />


খরচ রেজিস্টার করুন - প্রতিটি খরচ add করুন (খাবার, পরিবহন, বিদ্যুৎ ইত্যাদি)
খরচ দেখুন - সবগুলো খরচের একটি লিস্ট
বিশ্লেষণ করুন - মোট খরচ কতো বোঝা
নিরাপদ রাখুন - লগইন করে আপনার তথ্য সুরক্ষিত রাখুন


🏗️ Project Structure (প্রজেক্ট কাঠামো)
Family_expendeture/
│
├── core/                          # Django প্রজেক্ট সেটিংস
│   ├── settings.py               # প্রজেক্ট configuration
│   ├── urls.py                   # মেইন URL routing
│   └── wsgi.py                   # Server configuration
│
├── expenses/                      # খরচ ম্যানেজমেন্ট App
│   ├── models.py                 # ডেটাবেস মডেল
│   ├── views.py                  # Business logic
│   ├── urls.py                   # খরচ সম্পর্কিত URLs
│   ├── forms.py                  # Form handling
│   ├── admin.py                  # Django Admin
│   └── templates/
│       └── expenses/
│           ├── home.html         # হোম পেজ
│           ├── add_expense.html  # নতুন খরচ যোগ করা
│           └── register.html     # নিবন্ধন পেজ
│
├── static/                       # CSS, JavaScript, Images
│   └── css/
│       └── style.css
│
├── manage.py                     # Django management script
└── db.sqlite3                    # ডেটাবেস ফাইল

🔄 কীভাবে কাজ করে? (Workflow)
ধাপ 1: User Registration (ব্যবহারকারী নিবন্ধন)
User opens website
    ↓
Clicks "Register"
    ↓
Form fills করে (Username, Password, Email)
    ↓
Django validates
    ↓
Database এ save হয়
    ↓
Registration সম্পন্ন
ধাপ 2: User Login (লগইন করা)
User visits home
    ↓
Login form দেখে
    ↓
Username & Password enter করে
    ↓
Django checks database
    ↓
Match হলে Home page দেখায়
    ↓
Mismatch হলে Error দেখায়
ধাপ 3: Add Expense (খরচ যোগ করা)
User clicks "+ Add New Expense"
    ↓
Form opens (Date, Category, Description, Amount)
    ↓
User fills form
    ↓
Django validates data
    ↓
Database এ save হয়
    ↓
Home page এ নতুন expense দেখা যায়
ধাপ 4: View Expenses (খরচ দেখা)
Home page load হয়
    ↓
Django queries database
    ↓
All expenses fetch করে
    ↓
Template এ render করে
    ↓
User দেখতে পায় সব খরচের লিস্ট

💾 Database Models (ডেটাবেস মডেল)
User Model
Django এর built-in User model ব্যবহার করে।
User
├── username          // ব্যবহারকারীর নাম
├── password         // পাসওয়ার্ড (encrypted)
├── email            // ইমেইল
└── date_joined      // যখন register করেছে
Expense Model
খরচ সংরক্ষণ করার জন্য custom model।
Expense
├── user             // কে খরচ করেছে (User এর সাথে link)
├── date             // কখন খরচ (Date field)
├── category         // কিসের জন্য খরচ (Text)
├── description      // খরচের বিবরণ (Text)
├── amount           // কতো টাকা খরচ (Number)
└── created_at       // কখন database এ add হয়েছে
models.py Example:
pythonfrom django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category} - {self.amount}"

📁 Key Files ব্যাখ্যা
1. settings.py - প্রজেক্ট কনফিগারেশন
pythonINSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',      # ইউজার সিস্টেম
    'expenses',                  # আমাদের app
    'crispy_forms',             # ফর্ম সুন্দর করতে
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',   # ডেটাবেস
    }
}
2. urls.py - URL Routing
pythonurlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),  # খরচ সম্পর্কিত URLs
]
3. models.py - ডেটাবেস Structure
pythonclass Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # এটা মানে: প্রতিটি খরচ একটি user এর সাথে যুক্ত
    
    date = models.DateField()
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
4. views.py - Business Logic
pythondef home(request):
    # ইউজার logged in কিনা চেক করো
    if not request.user.is_authenticated:
        return redirect('login')
    
    # ডেটাবেস থেকে সব খরচ নিয়ে আসো
    expenses = Expense.objects.filter(user=request.user)
    
    # মোট খরচ calculate করো
    total = sum([e.amount for e in expenses])
    
    # Template এ পাঠাও
    return render(request, 'expenses/home.html', {
        'expenses': expenses,
        'total_amount': total
    })

🔐 Security Features (নিরাপত্তা)
1. User Authentication

প্রতিটি ইউজার একাউন্ট দিয়ে লগইন করে
শুধুমাত্র নিজের খরচ দেখতে পারে

2. Password Encryption

পাসওয়ার্ড এনক্রিপ্টেড থাকে ডেটাবেসে
Raw password কখনো save হয় না

3. CSRF Protection

Form এ CSRF token থাকে
Unauthorized requests block হয়

4. Session Management

লগইন করলে session create হয়
Logout করলে session delete হয়


🚀 কিভাবে চালাবেন?
Requirement:
bashpip install django django-crispy-forms crispy-bootstrap5
Database Setup:
bashpython manage.py migrate
Create Admin User:
bashpython manage.py createsuperuser
Run Server:
bashpython manage.py runserver
Access:

Home: http://localhost:8000/
Admin: http://localhost:8000/admin/


📊 Data Flow Diagram
┌─────────────┐
│   Browser   │ ← User opens website
└──────┬──────┘
       │
       ↓
┌─────────────────────────┐
│  Django URL Router      │ ← URL check করে কোন view চালাবে
│ (urls.py)              │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  Django View            │ ← Business logic চালায়
│ (views.py)             │ ← Database query করে
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  Database               │ ← Data fetch/store করে
│ (db.sqlite3)           │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  Django Template        │ ← Data দিয়ে HTML তৈরি করে
│ (home.html)            │
└──────┬──────────────────┘
       │
       ↓
┌─────────────┐
│  Browser    │ ← Rendered HTML দেখায়
└─────────────┘

🎓 শেখার পয়েন্ট
এই প্রজেক্টে আপনি শিখেছেন:
✅ Django Project Setup - প্রজেক্ট কীভাবে তৈরি করতে হয়
✅ Models - ডেটাবেস টেবল কীভাবে define করতে হয়
✅ Views - Backend logic কীভাবে লিখতে হয়
✅ Templates - Dynamic HTML কীভাবে রেন্ডার করতে হয়
✅ User Authentication - লগইন সিস্টেম কীভাবে কাজ করে
✅ Forms - ইউজার ইনপুট কীভাবে হ্যান্ডেল করতে হয়
✅ Database Queries - ডেটাবেস থেকে ডেটা কীভাবে fetch করতে হয়

🔮 ভবিষ্যতের উন্নতি
যোগ করতে পারেন:

📈 Chart/Analytics - Pie chart, Bar chart দিয়ে analysis দেখান
🏷️ Tags - খরচে ট্যাগ যোগ করুন
📤 Export - Excel/PDF এ ডাউনলোড করুন
📱 Mobile App - মোবাইল version তৈরি করুন
📧 Email Notifications - মাসিক রিপোর্ট পাঠান
💱 Budget Planning - মাসের budget সেট করুন


❓ FAQ (সাধারণ প্রশ্ন)
Q: এটা কি cloud hosted?
A: এখন local machine এ চলছে। চাইলে Heroku/PythonAnywhere এ deploy করতে পারেন।
Q: কতজন user একসাথে ব্যবহার করতে পারবে?
A: SQLite unlimited users support করতে পারে, তবে বড় প্রজেক্টের জন্য PostgreSQL ব্যবহার করুন।
Q: ডেটা কি safe?
A: Django এর security features থাকায় কিছুটা safe। Production এর জন্য HTTPS, firewall ইত্যাদি যোগ করতে হবে।
Q: কাস্টমাইজ করতে পারি?
A: হ্যাঁ, সবকিছু কাস্টমাইজ করা যায়।

📚 সম্পর্কিত লিঙ্ক

Django Official Docs: https://docs.djangoproject.com/
Django Models: https://docs.djangoproject.com/en/stable/topics/db/models/
Django Views: https://docs.djangoproject.com/en/stable/topics/http/views/
Django Templates: https://docs.djangoproject.com/en/stable/topics/templates/

