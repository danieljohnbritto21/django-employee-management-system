# Quick Start Guide - 5 Minutes to Running

## ⚡ Super Quick Start (Windows)

### Option 1: Fastest (Automatic Setup)

**PowerShell (Recommended):**
```powershell
cd "d:\Employee Management System\employee_project"
.\setup.ps1
```

**Command Prompt:**
```cmd
cd d:\Employee Management System\employee_project
setup.bat
```

This will:
1. ✅ Activate virtual environment
2. ✅ Install dependencies
3. ✅ Create database migrations
4. ✅ Apply migrations
5. ✅ Collect static files

### Option 2: Manual Setup (5 Minutes)

```powershell
# 1. Navigate to project
cd "d:\Employee Management System\employee_project"

# 2. Activate environment
.\env\Scripts\Activate.ps1

# 3. Install requirements
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --noinput

# Done!
```

## 🚀 Run the Server

```powershell
python manage.py runserver
```

**Output:**
```
Django version 5.2.15, using settings 'employee_management.settings'
Starting development server at http://127.0.0.1:8000/
```

## 👤 Create Admin Account

In a **new PowerShell window** (keep the server running):

```powershell
# Activate environment first
cd "d:\Employee Management System\employee_project"
.\env\Scripts\Activate.ps1

# Create superuser
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: (your password)
Password (again): (confirm)
Superuser created successfully.
```

## 🌐 Access Application

Open your browser and visit:

| URL | Purpose |
|-----|---------|
| http://localhost:8000/accounts/register/ | Create new user |
| http://localhost:8000/accounts/login/ | Login |
| http://localhost:8000/ | Dashboard (after login) |
| http://localhost:8000/admin/ | Admin panel (use superuser) |

## ✅ Test Everything Works

### 1. Register User (2 min)
- Go to: http://localhost:8000/accounts/register/
- Fill in the form
- Click "Create Account"
- You'll be logged in automatically

### 2. Create Department (1 min)
- Click "Add Department" button
- Fill in: Department ID & Name
- Click "Save"

### 3. Add Employee (1 min)
- Click "Employees" → "Add Employee"
- Fill in details
- Select department
- Click "Save"

### 4. View Dashboard (1 min)
- You should see:
  - Employee count
  - Department count
  - Quick action buttons

## 📝 Quick Commands

```powershell
# Activate environment
.\env\Scripts\Activate.ps1

# Run server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Reset database (careful!)
del db.sqlite3
python manage.py migrate

# Exit/Deactivate
deactivate
```

## 🎯 First-Time User Flow

```
1. Register new account
   ↓
2. Login with credentials
   ↓
3. View Dashboard (shows stats)
   ↓
4. Add Department
   ↓
5. Add Employee
   ↓
6. View Employee List
   ↓
7. Search/Filter employees
   ↓
8. Edit or Delete as needed
```

## 🔧 Troubleshooting

### Q: "Port 8000 already in use"
```powershell
python manage.py runserver 8001
```

### Q: "Module not found"
```powershell
# Make sure environment is activated
.\env\Scripts\Activate.ps1
```

### Q: "No module named 'django'"
```powershell
pip install -r requirements.txt
```

### Q: Can't login after registering
- Make sure you're on a fresh database
- Try: `del db.sqlite3` and `python manage.py migrate`

## 📚 Next Steps

1. **Learn the system**: Use the app, add some test data
2. **Customize**: Edit templates in `templates/` folder
3. **Advanced**: Read DEPLOYMENT.md for production setup
4. **Reference**: Check COMMANDS.md for all available commands

## 📞 Need Help?

- **Setup issues?** → Check COMMANDS.md
- **Want to deploy?** → Read DEPLOYMENT.md
- **Full details?** → See README.md
- **All commands?** → Check COMMANDS.md

---

**You're all set! Your Employee Management System is ready! 🚀**

Visit http://localhost:8000 to get started.
