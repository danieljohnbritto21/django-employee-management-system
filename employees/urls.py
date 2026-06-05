from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/edit/<int:id>/', views.employee_edit, name='employee_edit'),
    path('employees/delete/<int:id>/', views.employee_delete, name='employee_delete'),

    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/edit/<int:id>/', views.department_edit, name='department_edit'),
    path('departments/delete/<int:id>/', views.department_delete, name='department_delete'),

    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),

    # Leave URLs
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/apply/', views.leave_apply, name='leave_apply'),
    path('leave/status/<int:id>/<str:status>/', views.leave_status_update, name='leave_status_update'),

    # Task URLs
    path('task/', views.task_list, name='task_list'),
    path('task/assign/', views.task_assign, name='task_assign'),
    path('task/edit/<int:id>/', views.task_edit, name='task_edit'),
    path('task/delete/<int:id>/', views.task_delete, name='task_delete'),

    # Notice URLs
    path('notice/', views.notice_list, name='notice_list'),
    path('notice/create/', views.notice_create, name='notice_create'),
    path('notice/edit/<int:id>/', views.notice_edit, name='notice_edit'),
    path('notice/delete/<int:id>/', views.notice_delete, name='notice_delete'),
]