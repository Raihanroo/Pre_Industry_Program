# 📬 Django Contact Form

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.9-092E20?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.11.9-3776AB?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**A beautiful, fully functional contact form with Django, form validation, and database integration.**

</div>

---

## 🎯 What is This?

A complete contact form solution that lets users submit messages through an elegant web interface. All submissions are validated, stored in a database, and manageable through a secure admin dashboard.



---

## ✨ Features

- 📝 **User-Friendly Form** - Clean, responsive contact form
- ✅ **Form Validation** - Real-time email and field validation
- 💾 **Database Storage** - All messages saved with timestamps
- 🎨 **Beautiful UI** - Purple gradient design with smooth animations
- 📱 **Mobile Responsive** - Works on all devices
- 🔐 **Secure** - CSRF protection and input validation
- 🛡️ **Admin Dashboard** - Manage messages easily
- 📊 **Search & Filter** - Find messages by date, name, or email

---

## 🚀 Quick Start

### 1. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 2. Install Django
```bash
pip install django==5.2.9
```

### 3. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin Account
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

### 6. Access Application
- **Contact Form:** http://127.0.0.1:8000/contact/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
django-contact-form/
├── my_app/
│   ├── migrations/          # Database changes
│   ├── templates/
│   │   ├── contact.html     # Main form
│   │   └── success.html     # Success page
│   ├── models.py            # Message model
│   ├── forms.py             # Form validation
│   ├── views.py             # Business logic
│   └── admin.py             # Admin setup
├── my_site/
│   ├── settings.py          # Configuration
│   ├── urls.py              # URL routing
│   └── ...
├── manage.py
├── db.sqlite3               # Database
└── requirements.txt
```

---

## 📊 Database Schema

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique identifier |
| name | CharField | Sender's name (max 100) |
| email | EmailField | Sender's email |
| message | TextField | Message content |
| created_at | DateTime | Auto-generated timestamp |

---

## 🎨 How It Works

1. **User visits** `/contact/` page
2. **Fills form** with name, email, and message
3. **Form validates** email format automatically
4. **Submits form** - data sent to server
5. **Database saves** message with timestamp
6. **Success message** displays to user
7. **Admin views** all messages in dashboard

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| **Table not found** | Run `python manage.py migrate` |
| **CSRF token missing** | Add `{% csrf_token %}` in form |
| **Static files not loading** | Run `python manage.py collectstatic` |
| **Port 8000 in use** | Use `python manage.py runserver 8001` |
| **Module not found** | Run `pip install django==5.2.9` |

---

## 📖 File Descriptions

- **models.py** - Defines Message database model
- **forms.py** - Creates MessageForm with validation rules
- **views.py** - Handles form processing logic
- **admin.py** - Configures admin interface
- **contact.html** - User-facing form template
- **success.html** - Success confirmation page

---

## 🛡️ Security Features

✓ CSRF token protection  
✓ Email format validation  
✓ SQL injection prevention (using ORM)  
✓ XSS protection (template auto-escaping)  
✓ Admin authentication required  

---

## 📞 Support

- 🐛 Found a bug? Open an issue
- 💡 Have an idea? Submit a pull request
- 📧 Email: support@example.com

---

<div align="center">

**⭐ If you found this helpful, please star the repository!**

Made with ❤️ | MIT License | January 2026

</div>
