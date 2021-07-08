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

]

