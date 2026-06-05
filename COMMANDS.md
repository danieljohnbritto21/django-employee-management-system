# Django Employee Management System - Commands Reference

## Initial Setup Commands

### 1. Activate Virtual Environment
**Windows PowerShell:**
```
.\env\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```
.\env\Scripts\activate.bat
```

**Mac/Linux:**
```
source env/bin/activate
```

### 2. Install Requirements
```
pip install -r requirements.txt
```

### 3. Create Database Migrations
```
python manage.py makemigrations
```

### 4. Apply Migrations to Database
```
python manage.py migrate
```

### 5. Create Superuser (Admin)
```
python manage.py createsuperuser
```

Prompts:
- Username: admin
- Email: admin@example.com
- Password: (enter secure password)

### 6. Collect Static Files
```
python manage.py collectstatic --noinput
```

## Running the Application

### Start Development Server
```
python manage.py runserver
```

Server runs on: http://localhost:8000

### Alternative Ports
```
python manage.py runserver 8001
python manage.py runserver 0.0.0.0:8000
```

## Access Points

- Main Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- Login: http://localhost:8000/accounts/login/
- Register: http://localhost:8000/accounts/register/
- Dashboard: http://localhost:8000/
- Employees: http://localhost:8000/employees/
- Departments: http://localhost:8000/departments/

## Database Management

### Reset Database
```
# Delete existing database
del db.sqlite3  (Windows)
rm db.sqlite3   (Mac/Linux)

# Recreate database
python manage.py migrate
```

### Database Shell
```
python manage.py dbshell
```

## Django Admin Commands

### Create Admin User
```
python manage.py createsuperuser
```

### Change Admin Password
```
python manage.py changepassword admin
```

### Create Test Data
```
python manage.py shell
```

Then in Python shell:
```python
from django.contrib.auth.models import User
from employees.models import Department, Employee
from decimal import Decimal

# Create user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User'
)

# Create department
dept = Department.objects.create(
    department_id='IT',
    department_name='Information Technology'
)

# Create employee
emp = Employee.objects.create(
    name='John Doe',
    email='john@example.com',
    department=dept,
    salary=Decimal('50000.00')
)

print("Test data created successfully!")
```

Exit shell: `exit()`

## Useful Django Commands

### Check Settings
```
python manage.py check
```

### Run Tests
```
python manage.py test
```

### Run Specific App Tests
```
python manage.py test employees
python manage.py test accounts
```

### Show Database Migrations
```
python manage.py showmigrations
```

### SQL for Specific Migration
```
python manage.py sqlmigrate employees 0001
```

### Custom Django Shell
```
python manage.py shell_plus
```

## Static Files

### Collect Static Files
```
python manage.py collectstatic
```

### Clear Static Files
```
python manage.py collectstatic --clear --noinput
```

### Find Static Files
```
python manage.py findstatic style.css
```

## Debugging Commands

### Run with Debug
```
python manage.py runserver --debug
```

### Check URL Patterns
```
python manage.py show_urls
```

### Validate Templates
```
python manage.py validate_templates
```

## Creating New Items via Django Shell

### Create User
```python
from django.contrib.auth.models import User

user = User.objects.create_user(
    username='username',
    email='email@example.com',
    password='password',
    first_name='First',
    last_name='Last'
)
```

### Create Department
```python
from employees.models import Department

dept = Department.objects.create(
    department_id='DEPT001',
    department_name='Sales'
)
```

### Create Employee
```python
from employees.models import Employee
from decimal import Decimal

emp = Employee.objects.create(
    name='Jane Smith',
    email='jane@example.com',
    department=dept,
    salary=Decimal('60000.00')
)
```

### List All Employees
```python
from employees.models import Employee
employees = Employee.objects.all()
for emp in employees:
    print(f"{emp.name} - {emp.department.department_name}")
```

### Update Employee
```python
from employees.models import Employee
emp = Employee.objects.get(id=1)
emp.salary = 65000
emp.save()
```

### Delete Employee
```python
from employees.models import Employee
emp = Employee.objects.get(id=1)
emp.delete()
```

## Export Commands

### Export Database
```
python manage.py dumpdata > data.json
```

### Import Database
```
python manage.py loaddata data.json
```

### Export Specific App
```
python manage.py dumpdata employees > employees_data.json
```

## Performance and Optimization

### Run Django Optimizations
```
python manage.py optimize
```

### Check for Issues
```
python manage.py check --deploy
```

## Troubleshooting Commands

### Remove Migrations (Careful!)
```
# For specific app
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
```

### Reset App Migrations
```
python manage.py migrate employees zero
```

### Fix Missing Migrations
```
python manage.py makemigrations
python manage.py migrate --fake-initial
```

## Development Workflow

```bash
# 1. Activate environment
.\env\Scripts\Activate.ps1

# 2. Make changes to models
# (Edit employees/models.py)

# 3. Create migrations
python manage.py makemigrations

# 4. Apply migrations
python manage.py migrate

# 5. Run server
python manage.py runserver

# 6. Test in browser
# Navigate to http://localhost:8000

# 7. Deactivate when done
deactivate
```

## Quick Start (One-Liner Commands)

```bash
# Setup and run
.\env\Scripts\Activate.ps1 && python manage.py migrate && python manage.py runserver

# Full reset
del db.sqlite3 && python manage.py migrate && python manage.py createsuperuser

# Collect static and run
python manage.py collectstatic --noinput && python manage.py runserver
```

## Environment Variables (For Production)

Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Load with:
```python
import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv('DEBUG', False)
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
```

## Backup Database

```bash
# Windows
copy db.sqlite3 db.sqlite3.backup

# Mac/Linux
cp db.sqlite3 db.sqlite3.backup
```

## Restore Database

```bash
# Windows
copy db.sqlite3.backup db.sqlite3

# Mac/Linux
cp db.sqlite3.backup db.sqlite3
```

## Port Already in Use

```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000

# Mac/Linux:
lsof -i :8000

# Kill process
# Windows:
taskkill /PID <PID> /F

# Mac/Linux:
kill -9 <PID>

# Or just use different port:
python manage.py runserver 8001
```

## Useful Keyboard Shortcuts

| Command | Description |
|---------|-------------|
| Ctrl+C | Stop server |
| Ctrl+D | Exit Django shell |
| ↑ Arrow | Previous command in shell |
| Tab | Auto-complete in shell |

---

**Note:** Always activate virtual environment before running commands!
