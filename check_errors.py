"""
Comprehensive validation script for Employee Management System.
Tests ALL modules: GET pages, POST submissions, data integrity.
"""
import os, sys, datetime, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,testserver'
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from employees.models import Employee, Department, Attendance, Leave, Task, Notice

# ── Setup ──────────────────────────────────────────────────────────────────────
client = Client(SERVER_NAME='localhost', raise_request_exception=True)
user, _ = User.objects.get_or_create(username='admin', defaults={'is_superuser': True, 'is_staff': True})
if not user.has_usable_password():
    user.set_password('admin123')
    user.save()
client.force_login(user)

today = datetime.date.today().strftime('%Y-%m-%d')
PASS = 0
FAIL = 0

def check(label, ok, detail=''):
    global PASS, FAIL
    if ok:
        PASS += 1
        print("  PASS  %s" % label)
    else:
        FAIL += 1
        print("  FAIL  %s  -- %s" % (label, detail))

def test_get(url, expected=200):
    r = client.get(url)
    check("GET %-35s -> %d" % (url, expected), r.status_code == expected,
          "got %d" % r.status_code)
    return r

def test_post(url, data, expected_redirect=None):
    r = client.post(url, data, follow=True)
    ok = (r.status_code == 200)
    check("POST %-34s -> 200" % url, ok, "got %d" % r.status_code)
    return r

# ── Seed test data ─────────────────────────────────────────────────────────────
print("\n[1] Seeding test data...")
dept, _ = Department.objects.get_or_create(
    department_id='TEST01',
    defaults={'department_name': 'Test Department'}
)
emp, _ = Employee.objects.get_or_create(
    email='validation@example.com',
    defaults={'name': 'Validation Employee', 'department': dept}
)
check("Department exists (id=%s)" % dept.id, dept.id is not None)
check("Employee exists  (id=%s)" % emp.id, emp.id is not None)
check("Employee has auto ID", bool(emp.employee_id))

# ── GET pages ─────────────────────────────────────────────────────────────────
print("\n[2] Testing all GET pages...")
test_get('/')
test_get('/employees/')
test_get('/employees/add/')
test_get('/employees/edit/%d/' % emp.id)
test_get('/departments/')
test_get('/departments/add/')
test_get('/attendance/')
test_get('/attendance/mark/')
test_get('/leave/')
test_get('/leave/apply/')
test_get('/task/')
test_get('/task/assign/')
test_get('/notice/')
test_get('/notice/create/')

# ── POST: Attendance ───────────────────────────────────────────────────────────
print("\n[3] Testing POST - Mark Attendance...")
r = test_post('/attendance/mark/', {
    'employee': emp.id,
    'date': today,
    'check_in': '09:00',
    'check_out': '17:00',
})
att_exists = Attendance.objects.filter(employee=emp, date=today).exists()
check("Attendance record saved to DB", att_exists)

# Update same record (should not raise IntegrityError)
r2 = test_post('/attendance/mark/', {
    'employee': emp.id,
    'date': today,
    'check_in': '09:30',
    'check_out': '17:30',
})
check("Duplicate attendance update (no IntegrityError)", r2.status_code == 200,
      "got %d" % r2.status_code)

# ── POST: Leave Application ────────────────────────────────────────────────────
print("\n[4] Testing POST - Apply Leave...")
Leave.objects.filter(employee=emp, leave_type='Validation Leave').delete()
r = test_post('/leave/apply/', {
    'employee': emp.id,
    'leave_type': 'Validation Leave',
    'start_date': today,
    'end_date': today,
    'reason': 'Automated validation test',
})
leave_exists = Leave.objects.filter(employee=emp, leave_type='Validation Leave').exists()
check("Leave record saved to DB", leave_exists)

# ── POST: Leave Status Update ──────────────────────────────────────────────────
print("\n[5] Testing Leave Status Update...")
leave = Leave.objects.filter(employee=emp).first()
if leave:
    r = client.get('/leave/status/%d/Approved/' % leave.id, follow=True)
    check("GET leave status update -> 200", r.status_code == 200, "got %d" % r.status_code)
    leave.refresh_from_db()
    check("Leave status changed to Approved", leave.status == 'Approved',
          "status=%s" % leave.status)
else:
    check("Leave record exists for status update", False, "no leave found")

# ── POST: Assign Task ──────────────────────────────────────────────────────────
print("\n[6] Testing POST - Assign Task...")
Task.objects.filter(title='Validation Task').delete()
r = test_post('/task/assign/', {
    'title': 'Validation Task',
    'description': 'Testing task assignment',
    'assigned_to': emp.id,
    'priority': 'High',
    'status': 'Pending',
    'due_date': today,
})
task_exists = Task.objects.filter(title='Validation Task').exists()
check("Task record saved to DB", task_exists)

# ── POST: Task Edit ────────────────────────────────────────────────────────────
print("\n[7] Testing Task Edit...")
task = Task.objects.filter(title='Validation Task').first()
if task:
    r = test_post('/task/edit/%d/' % task.id, {
        'title': 'Validation Task Updated',
        'description': 'Updated description',
        'assigned_to': emp.id,
        'priority': 'Medium',
        'status': 'In Progress',
        'due_date': today,
    })
    task.refresh_from_db()
    check("Task status updated to In Progress", task.status == 'In Progress',
          "status=%s" % task.status)
else:
    check("Task exists for edit", False, "no task found")

# ── POST: Create Notice ────────────────────────────────────────────────────────
print("\n[8] Testing POST - Create Notice...")
Notice.objects.filter(title='Validation Notice').delete()
r = test_post('/notice/create/', {
    'title': 'Validation Notice',
    'content': 'This is an automated validation notice.',
    'is_published': True,
})
notice_exists = Notice.objects.filter(title='Validation Notice').exists()
check("Notice record saved to DB", notice_exists)

# Notice board should now show the notice
r2 = test_get('/notice/')
check("Notice board loads after creating notice", r2.status_code == 200)

# ── POST: Notice Edit ──────────────────────────────────────────────────────────
print("\n[9] Testing Notice Edit...")
notice = Notice.objects.filter(title='Validation Notice').first()
if notice:
    r = test_post('/notice/edit/%d/' % notice.id, {
        'title': 'Validation Notice Edited',
        'content': 'Updated content.',
        'is_published': False,
    })
    notice.refresh_from_db()
    check("Notice title updated", notice.title == 'Validation Notice Edited',
          "title=%s" % notice.title)
    check("Notice unpublished (draft)", not notice.is_published)
else:
    check("Notice exists for edit", False, "no notice found")

# ── Employee CRUD ──────────────────────────────────────────────────────────────
print("\n[10] Testing Employee Add/Edit/Delete...")
Employee.objects.filter(email='crud_test@example.com').delete()
r = test_post('/employees/add/', {
    'name': 'CRUD Test Employee',
    'email': 'crud_test@example.com',
    'mobile_number': '9876543210',
    'department': dept.id,
    'designation': 'Tester',
    'date_of_joining': today,
    'employment_status': 'Active',
    'address': '123 Test Street',
    'role': 'Employee',
})
new_emp = Employee.objects.filter(email='crud_test@example.com').first()
check("Employee added via form", new_emp is not None)

if new_emp:
    r2 = test_post('/employees/edit/%d/' % new_emp.id, {
        'name': 'CRUD Test Employee Updated',
        'email': 'crud_test@example.com',
        'mobile_number': '9876543210',
        'department': dept.id,
        'designation': 'Senior Tester',
        'date_of_joining': today,
        'employment_status': 'Active',
        'address': '123 Test Street',
        'role': 'HR',
    })
    new_emp.refresh_from_db()
    check("Employee role updated to HR", new_emp.role == 'HR', "role=%s" % new_emp.role)

    r3 = test_post('/employees/delete/%d/' % new_emp.id, {})
    still_exists = Employee.objects.filter(email='crud_test@example.com').exists()
    check("Employee deleted successfully", not still_exists)

# ── Department CRUD ────────────────────────────────────────────────────────────
print("\n[11] Testing Department Add/Edit/Delete...")
Department.objects.filter(department_id='CRUDTEST').delete()
r = test_post('/departments/add/', {
    'department_id': 'CRUDTEST',
    'department_name': 'CRUD Test Dept',
})
new_dept = Department.objects.filter(department_id='CRUDTEST').first()
check("Department added via form", new_dept is not None)

if new_dept:
    r2 = test_post('/departments/edit/%d/' % new_dept.id, {
        'department_id': 'CRUDTEST',
        'department_name': 'CRUD Test Dept Updated',
    })
    new_dept.refresh_from_db()
    check("Department name updated", 'Updated' in new_dept.department_name,
          "name=%s" % new_dept.department_name)

    r3 = test_post('/departments/delete/%d/' % new_dept.id, {})
    still_exists = Department.objects.filter(department_id='CRUDTEST').exists()
    check("Department deleted successfully", not still_exists)

# ── Model integrity ────────────────────────────────────────────────────────────
print("\n[12] Checking model integrity...")
check("Employee model has no profile_photo", not hasattr(Employee, 'profile_photo'))
check("Employee model has employee_id",      hasattr(Employee, 'employee_id'))
check("Notice model has is_published",       hasattr(Notice,   'is_published'))
check("Leave model has status choices",      hasattr(Leave,    'STATUS_CHOICES'))
check("Task model has priority choices",     hasattr(Task,     'PRIORITY_CHOICES'))

# ── Summary ────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
total = PASS + FAIL
print("RESULTS: %d/%d passed" % (PASS, total))
if FAIL == 0:
    print("ALL TESTS PASSED - System is fully functional!")
else:
    print("%d test(s) FAILED - see details above." % FAIL)
print("="*60)
