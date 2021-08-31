from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    path('api/student_lessons', views.student_lessons),
    path('api/student_lessons_year', views.student_lessons_year),
    path('api/student_lessons_month', views.student_lessons_month),
    path('api/student_lessons_week', views.student_lessons_week),
    path('api/student_subjects_lessons', views.student_subjects_lessons),

    path('api/employee_lessons', views.employee_lessons),
    path('api/employee_lessons_week', views.employee_lessons_week),
    path('api/employee_lessons_month', views.employee_lessons_month),
    path('api/employee_lessons_year', views.employee_lessons_year),
    path('api/employee_subjects_lessons', views.employee_subjects_lessons),

    path('api/parent_lessons', views.parent_lessons),
    path('api/parent_lessons_year', views.parent_lessons_year),
    path('api/parent_lessons_month', views.parent_lessons_month),
    path('api/parent_lessons_week', views.parent_lessons_week),
    path('api/parent_subjects_lessons', views.parent_subjects_lessons),

    path('api/manager_lessons', views.manager_lessons),

    path('api/manager_student_lessons', views.manager_student_lessons),
    path('api/manager_student_lessons_year', views.manager_student_lessons_year),
    path('api/manager_student_lessons_month', views.manager_student_lessons_month),
    path('api/manager_student_lessons_week', views.manager_student_lessons_week),
    path('api/manager_student_subjects_lessons', views.manager_student_subjects_lessons),

    path('api/manager_employee_lessons', views.manager_employee_lessons),
    path('api/manager_employee_lessons_year', views.manager_employee_lessons_year),
    path('api/manager_employee_lessons_month', views.manager_employee_lessons_month),
    path('api/manager_employee_lessons_week', views.manager_employee_lessons_week),
    path('api/manager_employee_subjects_lessons', views.manager_employee_subjects_lessons),

    path('api/corporation_lessons_year', views.corporation_lessons_year),
    path('api/corporation_lessons_month', views.corporation_lessons_month),
    path('api/corporation_lessons_week', views.corporation_lessons_week),
    path('api/corporation_subjects_lessons', views.corporation_subjects_lessons),
    path('api/corporation_students_lessons', views.corporation_students_lessons),
    
]
