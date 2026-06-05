from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Employee, Department, Attendance, Leave, Task, Notice
from .forms import (
    EmployeeForm, DepartmentForm, SearchForm,
    AttendanceForm, LeaveForm, TaskForm, NoticeForm
)
from django.core.paginator import Paginator


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def dashboard(request):
    try:
        today = timezone.now().date()
        total_employees = Employee.objects.count()
        present_today = Attendance.objects.filter(
            date=today, check_in__isnull=False
        ).values('employee').distinct().count()
        on_leave = Leave.objects.filter(
            start_date__lte=today, end_date__gte=today, status='Approved'
        ).count()
        pending_tasks = Task.objects.filter(status='Pending').count()
        recent_notices = Notice.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]

        context = {
            'total_employees': total_employees,
            'present_today': present_today,
            'on_leave': on_leave,
            'pending_tasks': pending_tasks,
            'recent_notices': recent_notices,
        }
    except Exception as e:
        messages.error(request, f'Dashboard error: {e}')
        context = {
            'total_employees': 0,
            'present_today': 0,
            'on_leave': 0,
            'pending_tasks': 0,
            'recent_notices': [],
        }
    return render(request, 'employees/dashboard.html', context)


# ─── Employees ────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def employee_list(request):
    employees_list = Employee.objects.select_related('department').all()
    search_form = SearchForm(request.GET or None)

    if search_form.is_valid():
        q = search_form.cleaned_data.get('search_query')
        dept = search_form.cleaned_data.get('department')
        if q:
            employees_list = employees_list.filter(
                Q(name__icontains=q) | Q(email__icontains=q) | Q(employee_id__icontains=q)
            )
        if dept:
            employees_list = employees_list.filter(department=dept)

    paginator = Paginator(employees_list, 10)
    employees = paginator.get_page(request.GET.get('page'))
    return render(request, 'employees/list.html', {
        'employees': employees,
        'search_form': search_form
    })


@login_required(login_url='login')
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm()
    return render(request, 'employees/add.html', {'form': form, 'title': 'Add Employee'})


@login_required(login_url='login')
def employee_edit(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/add.html', {
        'form': form, 'employee': employee, 'title': 'Edit Employee'
    })


@login_required(login_url='login')
def employee_delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'employee': employee})


# ─── Departments ──────────────────────────────────────────────────────────────

@login_required(login_url='login')
def department_list(request):
    departments = Department.objects.annotate(employee_count=Count('employees'))
    return render(request, 'employees/department_list.html', {'departments': departments})


@login_required(login_url='login')
def department_add(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully!')
            return redirect('department_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm()
    return render(request, 'employees/add_department.html', {'form': form, 'title': 'Add Department'})


@login_required(login_url='login')
def department_edit(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('department_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'employees/add_department.html', {
        'form': form, 'department': department, 'title': 'Edit Department'
    })


@login_required(login_url='login')
def department_delete(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('department_list')
    return render(request, 'employees/confirm_delete_dept.html', {'department': department})


# ─── Attendance ───────────────────────────────────────────────────────────────

@login_required(login_url='login')
def attendance_list(request):
    attendances = Attendance.objects.select_related('employee').all().order_by('-date')
    paginator = Paginator(attendances, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'employees/attendance_list.html', {'attendances': page_obj})


@login_required(login_url='login')
def attendance_mark(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            att_date = form.cleaned_data['date']
            # update_or_create prevents IntegrityError on duplicate employee+date
            attendance, created = Attendance.objects.update_or_create(
                employee=employee,
                date=att_date,
                defaults={
                    'check_in': form.cleaned_data.get('check_in'),
                    'check_out': form.cleaned_data.get('check_out'),
                }
            )
            msg = 'Attendance marked successfully!' if created else 'Attendance record updated!'
            messages.success(request, msg)
            return redirect('attendance_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AttendanceForm()
    return render(request, 'employees/form_generic.html', {
        'form': form,
        'title': 'Mark Attendance',
        'submit_label': 'Mark Attendance',
        'back_url': 'attendance_list',
    })


# ─── Leave ────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def leave_list(request):
    leaves = Leave.objects.select_related('employee').all().order_by('-applied_on')
    paginator = Paginator(leaves, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'employees/leave_list.html', {'leaves': page_obj})


@login_required(login_url='login')
def leave_apply(request):
    """
    Apply for leave. The form includes an employee selector so any user
    (including admin/superuser without a linked Employee record) can submit.
    """
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Leave applied successfully!')
            return redirect('leave_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LeaveForm()
        # Pre-select current user's employee if linked
        linked_employee = getattr(request.user, 'employee', None)
        if linked_employee:
            form.fields['employee'].initial = linked_employee

    return render(request, 'employees/form_generic.html', {
        'form': form,
        'title': 'Apply for Leave',
        'submit_label': 'Submit Application',
        'back_url': 'leave_list',
    })


@login_required(login_url='login')
def leave_status_update(request, id, status):
    leave = get_object_or_404(Leave, id=id)
    allowed = dict(Leave.STATUS_CHOICES)
    if status in allowed:
        leave.status = status
        leave.save()
        messages.success(request, f'Leave {status.lower()} successfully!')
    else:
        messages.error(request, 'Invalid status value.')
    return redirect('leave_list')


# ─── Tasks ────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.select_related('assigned_to', 'assigned_by').all().order_by('-created_at')
    paginator = Paginator(tasks, 15)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'employees/task_list.html', {'tasks': page_obj})


@login_required(login_url='login')
def task_assign(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            # assigned_by is nullable — only set if user has a linked Employee
            task.assigned_by = getattr(request.user, 'employee', None)
            task.save()
            messages.success(request, 'Task assigned successfully!')
            return redirect('task_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm()
    return render(request, 'employees/form_generic.html', {
        'form': form,
        'title': 'Assign Task',
        'submit_label': 'Assign Task',
        'back_url': 'task_list',
    })


@login_required(login_url='login')
def task_edit(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'employees/form_generic.html', {
        'form': form,
        'title': 'Edit Task',
        'submit_label': 'Update Task',
        'back_url': 'task_list',
    })


@login_required(login_url='login')
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'employees/confirm_delete_generic.html', {
        'object': task, 'title': 'Delete Task', 'cancel_url': 'task_list'
    })


# ─── Notices ──────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    paginator = Paginator(notices, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'employees/notice_list.html', {'notices': page_obj})


@login_required(login_url='login')
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            # created_by is nullable — only set if user has a linked Employee
            notice.created_by = getattr(request.user, 'employee', None)
            notice.save()
            messages.success(request, 'Notice created successfully!')
            return redirect('notice_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoticeForm()
    return render(request, 'employees/form_generic.html', {
        'form': form,
        'title': 'Create Notice',
        'submit_label': 'Publish Notice',
        'back_url': 'notice_list',
    })


@login_required(login_url='login')
def notice_edit(request, id):
    notice = get_object_or_404(Notice, id=id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully!')
            return redirect('notice_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'employees/form_generic.html', {
        'form': form,
        'title': 'Edit Notice',
        'submit_label': 'Save Changes',
        'back_url': 'notice_list',
    })


@login_required(login_url='login')
def notice_delete(request, id):
    notice = get_object_or_404(Notice, id=id)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('notice_list')
    return render(request, 'employees/confirm_delete_generic.html', {
        'object': notice, 'title': 'Delete Notice', 'cancel_url': 'notice_list'
    })