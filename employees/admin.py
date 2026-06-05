from django.contrib import admin
from .models import Employee, Department, Attendance, Leave, Task, Notice


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name', 'created_at')
    search_fields = ('department_id', 'department_name')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'email', 'department', 'designation', 'employment_status', 'role')
    list_filter = ('employment_status', 'role', 'department')
    search_fields = ('name', 'email', 'employee_id')
    # profile_photo removed


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out')
    list_filter = ('date',)
    search_fields = ('employee__name',)


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_on')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'assigned_by', 'priority', 'status', 'due_date')
    list_filter = ('priority', 'status')
    search_fields = ('title', 'assigned_to__name')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title',)