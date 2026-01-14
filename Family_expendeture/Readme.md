=== This is a Django Project ===

## Family Expenditure Tracker 

The core concepts of the Project: Its online expenditure tracking system
such as: registered family members & personal expenditure to save in the database, and anytime users can visualise their expenditure 


## Projects Visual Flow 
From the beginning, you have to create an Account on the Registration page.

<img width="1336" height="820" alt="image" src="https://github.com/user-attachments/assets/58ddb28c-cd23-4076-be40-bf927501ffe3" />

After registration, your family login form will appear, and then fill in your username and password 

<img width="1167" height="704" alt="image" src="https://github.com/user-attachments/assets/10a554aa-bfb2-43a3-825d-8d15962bf970" />

As a member of the family, you will see your Family Dashboard like this 

<img width="1756" height="669" alt="image" src="https://github.com/user-attachments/assets/ed132a73-cf62-4b82-b8c6-fdd988fd11b5" />
Now, you will add your expenditure by clicking the "Add New Expenditure" button. Then you put your expenditure & press the Save to record button 

<img width="1348" height="830" alt="image" src="https://github.com/user-attachments/assets/ef1f7036-6920-4052-ab05-761f5a7aee8f" />

Your Family Dashboard will show your live expenditure, which was included with (date, Category, Description, Amount)  
Inside the dashboard/homepage, you have the Total Spending Heder where your whole day, month, or whenever you're adding your expenditure, the total spending money will be included here  

<img width="1621" height="621" alt="image" src="https://github.com/user-attachments/assets/cf78e7c0-0fc4-4137-9683-9b59871ff542" />

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














