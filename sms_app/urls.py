from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('students/', views.students, name='students'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('attendance/', views.attendance, name='attendance'),
    path('marks/', views.marks, name='marks'),
    path('fees/', views.fees, name='fees'),
    path('courses/', views.courses, name='courses'),


    path('admin-dashboard/',
        views.admin_dashboard),

    path('student-dashboard/',
        views.student_dashboard, name='student_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),

    path('teacher-login/', views.teacher_login, name='teacher_login'),

    path('student-login/', views.student_login, name='student_login'),
    path(
        'teacher-dashboard/',
        views.teacher_dashboard
    ),

    path('edit-attendance/<int:id>/',
        views.edit_attendance,
        name='edit_attendance'),

    path('delete-attendance/<int:id>/',
         views.delete_attendance,
        name='delete_attendance'),

    path('edit-marks/<int:id>/',
        views.edit_marks,
        name='edit_marks'),

    path('delete-marks/<int:id>/',
         views.delete_marks,
        name='delete_marks'),


    path('teacher/register/', views.teacher_register, name='teacher_register'),
    path(
        'download-report/<int:id>/',
        views.download_report,
        name='download_report'
    ),
    path(
        'edit-student-profile/',
        views.edit_student_profile,
        name='edit_student_profile'
    ),
]