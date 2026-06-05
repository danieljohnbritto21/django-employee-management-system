# Setup Verification & Testing Guide

## ✅ Pre-Setup Checklist

Before running setup, verify:

- [ ] Python 3.x installed (`python --version`)
- [ ] Virtual environment exists (`env/` folder)
- [ ] Internet connection available
- [ ] No port 8000 in use
- [ ] At least 500MB free disk space
- [ ] Administrator access (if needed)

## 🚀 Setup Execution Steps

### Step 1: Navigate to Project
```bash
cd "d:\Employee Management System\employee_project"
```

### Step 2: Run Setup (Choose One)

**Option A: PowerShell (Recommended)**
```powershell
.\setup.ps1
```

**Option B: Command Prompt**
```cmd
setup.bat
```

**Option C: Manual (See below)**

### Step 3: Create Superuser
```bash
python manage.py createsuperuser
```

Inputs:
```
Username: admin
Email: admin@example.com
Password: ••••••••
Password (again): ••••••••
```

### Step 4: Start Server
```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## 🔍 Verification Checklist

### Installation Verification
- [ ] Virtual environment activated
- [ ] Django installed (`pip show django`)
- [ ] All dependencies installed
- [ ] Database created (`db.sqlite3` exists)
- [ ] Migrations applied (no pending migrations)

### Database Verification
```bash
python manage.py showmigrations
```

Expected: All migrations marked with `[X]`

### Static Files Verification
```bash
python manage.py collectstatic --dry-run
```

Expected: Lists collected files

### Django Check
```bash
python manage.py check
```

Expected:
```
System check identified no issues (0 silenced).
```

## 🌐 Access Points Verification

### 1. Test Homepage (Dashboard)
- **URL**: http://localhost:8000/
- **Expected**: Redirects to login (because not authenticated)
- **Status**: ✅

### 2. Test Registration
- **URL**: http://localhost:8000/accounts/register/
- **Expected**: Registration form appears
- **Test**: 
  - Fill form
  - Click "Create Account"
  - Should be logged in

### 3. Test Login
- **URL**: http://localhost:8000/accounts/login/
- **Expected**: Login form
- **Test**:
  - Enter credentials
  - Click "Login"
  - Should see dashboard

### 4. Test Dashboard
- **URL**: http://localhost:8000/
- **Expected**: Dashboard with stats
- **Elements Should Show**:
  - Total Employees count
  - Total Departments count
  - Quick action buttons

### 5. Test Employees
- **URL**: http://localhost:8000/employees/
- **Expected**: Empty list (no employees yet)
- **Test**: Click "Add Employee"

### 6. Test Add Employee
- **URL**: http://localhost:8000/employees/add/
- **Expected**: Employee form
- **Test**:
  - Must have department first
  - Or create inline with modal

### 7. Test Departments
- **URL**: http://localhost:8000/departments/
- **Expected**: Empty list initially
- **Test**: Click "Add Department"

### 8. Test Add Department
- **URL**: http://localhost:8000/departments/add/
- **Expected**: Department form
- **Test**:
  - Fill Department ID: "IT"
  - Fill Name: "Information Technology"
  - Click "Save"

### 9. Test Admin Panel
- **URL**: http://localhost:8000/admin/
- **Expected**: Login required, then admin panel
- **Test**:
  - Login as superuser
  - View Users, Employees, Departments

## 📊 Feature Verification Checklist

### Authentication Features
- [ ] User can register new account
- [ ] Registered user can login
- [ ] Invalid credentials rejected
- [ ] Logged-in users see personalized navbar
- [ ] Logout button works
- [ ] Unauthorized users redirected to login

### Dashboard Features
- [ ] Displays total employee count
- [ ] Displays total department count
- [ ] Shows quick action buttons
- [ ] Responsive on mobile

### Employee Features
- [ ] Can add new employee
- [ ] Can view employee list
- [ ] Can edit employee
- [ ] Can delete employee (with confirmation)
- [ ] Search by name works
- [ ] Search by email works
- [ ] Filter by department works
- [ ] Display creation date

### Department Features
- [ ] Can add new department
- [ ] Can view department list
- [ ] Can edit department
- [ ] Can delete department (with confirmation)
- [ ] Modal for quick add works

### UI/UX Features
- [ ] Bootstrap styling applied
- [ ] Sidebar navigation works
- [ ] Navbar displays correctly
- [ ] Tables look professional
- [ ] Forms have proper validation
- [ ] Error messages display
- [ ] Success messages display
- [ ] Icons display correctly (Font Awesome)
- [ ] Responsive on mobile/tablet
- [ ] Responsive on desktop

## 🧪 Manual Testing Scenarios

### Scenario 1: New User Journey
```
1. Go to http://localhost:8000/accounts/register/
2. Fill registration form
   - Username: testuser
   - First Name: Test
   - Last Name: User
   - Email: test@example.com
   - Password: TestPass123!
   - Confirm: TestPass123!
3. Click "Create Account"
4. Should see dashboard
✅ Pass: User registered and logged in
```

### Scenario 2: Add Department
```
1. From dashboard, click "Add Department"
2. Fill form:
   - Department ID: HR
   - Department Name: Human Resources
3. Click "Save"
4. Should see department in list
✅ Pass: Department created
```

### Scenario 3: Add Employee
```
1. Click "Employees" → "Add Employee"
2. Fill form:
   - Name: John Doe
   - Email: john@example.com
   - Department: Human Resources
   - Salary: 50000.00
3. Click "Save"
4. Should see employee in list
✅ Pass: Employee created
```

### Scenario 4: Search Employee
```
1. Go to employee list
2. Type "John" in search box
3. Click "Search"
4. Should show only John Doe
✅ Pass: Search works
```

### Scenario 5: Edit Employee
```
1. Go to employee list
2. Click "Edit" on an employee
3. Change salary to 55000
4. Click "Save"
5. Should see updated salary
✅ Pass: Edit works
```

### Scenario 6: Delete Employee (with confirmation)
```
1. Go to employee list
2. Click "Delete" on an employee
3. Confirm by clicking "Delete" again
4. Employee should be removed
✅ Pass: Delete works
```

## 🐛 Troubleshooting Verification

### Issue: Port 8000 in use
**Verify:**
```bash
netstat -ano | findstr :8000
# If shows process, use different port:
python manage.py runserver 8001
```

### Issue: Database errors
**Verify:**
```bash
# Check migrations
python manage.py showmigrations

# Reapply migrations
python manage.py migrate --fake-initial

# Or reset
del db.sqlite3
python manage.py migrate
```

### Issue: Static files not loading
**Verify:**
```bash
python manage.py collectstatic
# Check if styles load: http://localhost:8000/static/css/style.css
```

### Issue: Can't login after register
**Verify:**
```bash
# Check user exists
python manage.py shell
from django.contrib.auth.models import User
User.objects.all()
exit()

# Or reset database and retry
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Templates not found
**Verify:**
- `templates/` folder exists
- Files are in correct subdirectories
- `TEMPLATES` setting in settings.py correct
- No typos in view render() calls

### Issue: Form not working
**Verify:**
```bash
python manage.py check
# Should show: "System check identified no issues"
```

## 📈 Performance Verification

### Database Queries
```bash
python manage.py shell
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    from employees.models import Employee
    list(Employee.objects.all())
    print(f"Queries: {len(ctx)}")
```

Expected: Minimal queries for each view

### Static Files Size
```bash
dir /s static\
```

Expected: Should be under 1MB

### Page Load Time
- Local development: < 500ms
- Dashboard: < 200ms
- List views: < 300ms

## ✅ Final Verification Checklist

Before declaring complete:

- [ ] Setup script ran successfully
- [ ] No migration errors
- [ ] Superuser created
- [ ] Server starts without errors
- [ ] Can access http://localhost:8000
- [ ] Can register new user
- [ ] Can login as registered user
- [ ] Can login as superuser
- [ ] Dashboard shows correct counts
- [ ] Can add department
- [ ] Can add employee
- [ ] Can view employee list
- [ ] Can search employees
- [ ] Can edit employee
- [ ] Can delete employee
- [ ] Can edit department
- [ ] Can delete department
- [ ] All buttons work
- [ ] All links work
- [ ] Responsive design works
- [ ] Bootstrap styling applied
- [ ] Messages display correctly
- [ ] No console errors
- [ ] No 404 errors
- [ ] No 500 errors

## 📞 Getting Help

### If Something Fails:

1. **Check logs:**
   ```bash
   # Django console shows errors
   # Look at terminal output
   ```

2. **Check specific errors:**
   ```bash
   python manage.py check --deploy
   ```

3. **Reset and retry:**
   ```bash
   del db.sqlite3
   python manage.py migrate
   ```

4. **Read documentation:**
   - README.md - Full docs
   - COMMANDS.md - Command reference
   - QUICK_START.md - Quick setup

5. **Check Django docs:**
   - https://docs.djangoproject.com/

## 🎉 Success Indicators

You know it's working when:

✅ Setup script completes without errors
✅ `python manage.py check` shows no issues
✅ Database has tables (check with `db.sqlite3`)
✅ Can access all URLs without 404
✅ Registration and login work
✅ Dashboard displays statistics
✅ Can create/edit/delete all items
✅ Search and filter work
✅ UI looks professional with Bootstrap
✅ No JavaScript errors in console
✅ Mobile view is responsive

---

## 🚀 You're All Set!

If all checkboxes are ✅, your Employee Management System is:
- ✅ Properly installed
- ✅ Correctly configured
- ✅ Fully functional
- ✅ Ready for use

**Congratulations! Your system is ready to manage employees! 🎉**

Next steps:
1. Add test data
2. Customize as needed
3. Read DEPLOYMENT.md for production
4. Explore Django documentation

---

**Questions?** See README.md or COMMANDS.md
