# Employee Management System - Django 5

A complete Django Employee Management System built with Django 5, SQLite, and Bootstrap 5.

## Features

### Authentication Module
- User Registration with validation
- User Login
- User Logout
- Password validation using Django's built-in validators
- Login required for all employee pages

### Dashboard
- Welcome page after login
- Total employees count
- Total departments count
- Quick action buttons
- Responsive navigation menu

### Employee Module
- Add new employees
- Edit existing employees
- Delete employees
- View employee list with pagination
- Search employees by name or email
- Filter employees by department
- Display employee creation date

### Department Module
- Add new departments
- Edit departments
- Delete departments
- View department list
- Bootstrap modal for adding departments

### UI Features
- Bootstrap 5 responsive design
- Sidebar navigation dashboard
- Bootstrap cards and tables
- Alert messages for user feedback
- Responsive navbar
- Font Awesome icons
- Professional color scheme

## Project Structure

```
employee_project/
├── manage.py
├── db.sqlite3
├── employee_management/       # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/                   # Authentication app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── employees/                  # Employee management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_department_alter_employee_department.py
├── templates/
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   └── employees/
│       ├── dashboard.html
│       ├── list.html
│       ├── add.html
│       ├── confirm_delete.html
│       ├── department_list.html
│       ├── add_department.html
│       └── confirm_delete_dept.html
└── static/
    └── css/
        └── style.css
```

## Installation & Setup

### 1. Navigate to Project Directory
```bash
cd d:\Employee\ Management\ System\employee_project
```

### 2. Activate Virtual Environment
**Windows (PowerShell):**
```bash
.\env\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
.\env\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install django==5.2.15
pip install sqlparse==0.5.5
```

### 4. Make Migrations
After updating the models, create migration files:
```bash
python manage.py makemigrations
```

### 5. Apply Migrations
Apply all migrations to create database tables:
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin)
Create an admin account to access Django admin:
```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 7. Collect Static Files
Collect all static files (CSS, JS, images):
```bash
python manage.py collectstatic --noinput
```

## Running the Application

### Start Development Server
```bash
python manage.py runserver
```

Server will start at: `http://localhost:8000`

### Access the Application
- **Main App:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **Login Page:** http://localhost:8000/accounts/login
- **Register Page:** http://localhost:8000/accounts/register

## Default Test Credentials

After creating a superuser:
- Navigate to http://localhost:8000/accounts/register
- Create a new user account
- Log in with your credentials

## Application URLs

### Authentication URLs
- `http://localhost:8000/accounts/login/` - Login page
- `http://localhost:8000/accounts/register/` - Registration page
- `http://localhost:8000/accounts/logout/` - Logout

### Employee URLs
- `http://localhost:8000/` - Dashboard
- `http://localhost:8000/employees/` - Employee list
- `http://localhost:8000/employees/add/` - Add new employee
- `http://localhost:8000/employees/edit/<id>/` - Edit employee
- `http://localhost:8000/employees/delete/<id>/` - Delete employee

### Department URLs
- `http://localhost:8000/departments/` - Department list
- `http://localhost:8000/departments/add/` - Add new department
- `http://localhost:8000/departments/edit/<id>/` - Edit department
- `http://localhost:8000/departments/delete/<id>/` - Delete department

## Database Schema

### Users Table (Django Auth)
- id (Primary Key)
- username (Unique)
- first_name
- last_name
- email
- password
- is_active

### Departments Table
- id (Primary Key)
- department_id (Unique)
- department_name
- created_at
- updated_at

### Employees Table
- id (Primary Key)
- name
- email (Unique)
- department_id (Foreign Key to Department)
- salary
- date_created
- updated_at

## Features Implemented

### ✅ Authentication Module
- [x] User Registration Page
- [x] User Login Page
- [x] User Logout
- [x] Password Validation
- [x] Login Required for all Employee Pages
- [x] Bootstrap form styling

### ✅ Dashboard
- [x] Welcome Page after Login
- [x] Total Employees Count
- [x] Total Departments Count
- [x] Navigation Menu
- [x] Quick Actions

### ✅ Department Module
- [x] Add Department
- [x] Edit Department
- [x] Delete Department (with confirmation)
- [x] Department List
- [x] Department ID
- [x] Department Name

### ✅ Employee Module
- [x] Add Employee
- [x] Edit Employee
- [x] Delete Employee (with confirmation)
- [x] Employee List
- [x] Search Employee by Name
- [x] Search Employee by Email
- [x] Filter Employee by Department

### ✅ Employee Fields
- [x] Employee ID (Auto-generated)
- [x] Employee Name
- [x] Email (Unique)
- [x] Department (ForeignKey)
- [x] Salary
- [x] Date Created

### ✅ UI Requirements
- [x] Bootstrap 5
- [x] Responsive Design
- [x] Navbar with user info
- [x] Sidebar Dashboard
- [x] Bootstrap Cards
- [x] Bootstrap Tables
- [x] Bootstrap Modal Popup for Add Department
- [x] Font Awesome Icons
- [x] Professional color scheme

### ✅ Django Features
- [x] Models with relationships
- [x] Forms and ModelForms
- [x] Function-based views
- [x] URL routing
- [x] Templates
- [x] Static files
- [x] Messages framework
- [x] Decorators (@login_required)

## Admin Panel

Access Django admin at: http://localhost:8000/admin

Manage:
- Users (Create, Edit, Delete)
- Employees
- Departments

## Troubleshooting

### 1. Port Already in Use
```bash
python manage.py runserver 8001
```

### 2. Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### 3. Database Errors
```bash
# Delete db.sqlite3 and recreate
python manage.py migrate
python manage.py createsuperuser
```

### 4. Module Not Found
Ensure virtual environment is activated:
```bash
pip install -r requirements.txt
```

## Security Notes

- ✅ CSRF protection enabled
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Password validation rules
- ✅ User authentication required
- ⚠️ Change SECRET_KEY in production
- ⚠️ Set DEBUG = False in production
- ⚠️ Use environment variables for sensitive data

## Technologies Used

- **Framework:** Django 5.2.15
- **Database:** SQLite3
- **Frontend:** Bootstrap 5.1.3
- **Icons:** Font Awesome 6.0
- **Python:** 3.x

## File Descriptions

### accounts/forms.py
- `RegisterForm` - User registration with email validation
- `LoginForm` - User login form

### accounts/views.py
- `register()` - Handle user registration
- `login_view()` - Handle user login
- `logout_view()` - Handle user logout

### employees/models.py
- `Department` - Department model with metadata
- `Employee` - Employee model with relationships

### employees/forms.py
- `EmployeeForm` - Form for adding/editing employees
- `DepartmentForm` - Form for managing departments
- `SearchForm` - Form for searching employees

### employees/views.py
- `dashboard()` - Main dashboard view
- `employee_list()` - List and search employees
- `employee_add()` - Add new employee
- `employee_edit()` - Edit existing employee
- `employee_delete()` - Delete employee with confirmation
- `department_list()` - List all departments
- `department_add()` - Add new department
- `department_edit()` - Edit existing department
- `department_delete()` - Delete department with confirmation

## Performance Tips

1. Use search filters to reduce data loading
2. Pagination recommended for large datasets
3. Index frequently searched fields
4. Use `select_related()` for foreign keys
5. Cache dashboard statistics

## Future Enhancements

- [ ] Employee salary reports
- [ ] Department-wise statistics
- [ ] Export to CSV/Excel
- [ ] Email notifications
- [ ] Advanced filtering
- [ ] Pagination
- [ ] API endpoints
- [ ] Dashboard analytics
- [ ] Bulk operations

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, refer to:
- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- SQLite Documentation: https://www.sqlite.org/docs.html

---

**Last Updated:** 2024
**Version:** 1.0
**Status:** Complete and Ready for Deployment
