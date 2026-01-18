=== This is a Django Project ===

## Family Expenditure Tracker 

The core concepts of the Project: Its online expenditure tracking system
such as: registered family members & personal expenditure to save in the database, and anytime users can visualise their expenditure 


## Projects Visual Flow 
From the beginning, you have to create an Account on the Registration page.

<img width="1264" height="823" alt="image" src="https://github.com/user-attachments/assets/2e7660fd-f987-412e-bae5-ed8e446ecd53" />

After registration, your family login form will appear, and then fill in your username and password 

<img width="1348" height="812" alt="image" src="https://github.com/user-attachments/assets/35b62aa3-cc59-48c6-8c88-96b0f30b3152" />


As a member of the family, you will see your Family Dashboard like this 

<img width="1562" height="821" alt="image" src="https://github.com/user-attachments/assets/fc92f9d7-d293-49cf-8665-a87d68b76c38" />

Now, you will add your expenditure by clicking the "Add New Expenditure" button. Then you put your expenditure & press the Save to record button, or if you want to edit or delete your current date, you can click the  edit button, then you will see the Update Expenditure like this and save the record

<img width="1035" height="730" alt="image" src="https://github.com/user-attachments/assets/6920287d-5c68-4e08-a462-72882785fa34" />

And if you click the delete button to remove your date from the dashboard, the pop-up button will show you for your permission, and if you press the ok button, the date will be removed from the dashboard 

<img width="1867" height="969" alt="image" src="https://github.com/user-attachments/assets/b196d64e-e662-4cf0-b3e5-be5e75f5a82e" />


Your Family Dashboard will show your live expenditure, which was included with (date, Category, Description, Amount)  
Inside the dashboard/homepage, you have the Total Spending Header where, for your whole day, month, or whenever you're adding your expenditure, the total spending money will be included here  

<img width="1562" height="821" alt="image" src="https://github.com/user-attachments/assets/fc92f9d7-d293-49cf-8665-a87d68b76c38" />


So, this is the common flow of the project, which is described here by using images 

 🎯 Project Main Goals
 1. Keep family expenses in one place
 2. Secure login protects data
 3. Organise expenses by category
 4. Know total spending anytime
 5. Help with future budgeting  

🚀 How to Run the App - Complete Guide
First Time Setup
# 1️⃣  Enter project folder
cd Family_expenditure

# 2️⃣  Create Virtual Environment
python -m venv venv

# 3️⃣  Activate Virtual Environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# 4️⃣  Install required packages
pip install django django-crispy-forms crispy-bootstrap5

# 5️⃣  Create database tables
python manage.py migrate

# 6️⃣  Create admin account
python manage.py createsuperuser
# Will ask for: Username, Email, Password

# 7️⃣  Start server
python manage.py runserver

# 8️⃣  Open in browser
# Home: http://localhost:8000/
# Admin: http://localhost:8000/admin/


Subsequent Runs
# Just run these two commands:

# 1️⃣  Activate Virtual Environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# 2️⃣  Start server
python manage.py runserver

# 3️⃣  Browser: http://localhost:8000/


🔐 Security Features
Feature
How it Works
Login System
Each user sees only their own data
Password Encryption
Passwords stored encrypted in the database
CSRF Token
Form submissions protected
Session Management
Session ends after logout
Data Isolation
Ahmed can't see Fatima's expenses

 Technology Details
Frontend (What users see):
├── HTML (page structure)
├── CSS (design)
└── JavaScript (interactions)

Backend (What runs on server):
├── Django (framework)
├── Python (programming language)
└── SQLite (database)

Data Flow:
Browser → Django Server → Database → Browser

Frequently Asked Questions
Q: What if I forget my password?
A: Currently no "Forgot Password" feature. Contact admin to reset your password.

Q: Can other users see my expenses?
A: No. Django's login system shows each user only their own data.

Q: What if data is lost?
A: Backup the db.sqlite3 file. You can recover it if lost.

Q: What expense categories exist?
A: Currently: MANIBACK, SHUCKS, SHOE, FOOD, etc. Can add more as needed.

📞 Troubleshooting
Problem
Solution
Server won't start
Try python manage.py runserver again
Port 8000 in use
Use python manage.py runserver 8001
No database tables
Run python manage.py migrate
Can't login
Check Username and Password

🎓 What I Learned
This project teaches me:
✅ Django Project Setup
✅ Models (Database Structure)
✅ Views (Business Logic)
✅ Templates (HTML Rendering)
✅ Forms (User Input)
✅ User Authentication (Login System)
✅ Database Queries (Fetching Data)
✅ Validation (Data Checking)














