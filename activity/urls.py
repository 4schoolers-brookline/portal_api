from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('api/student_lessons', views.student_lessons),
    path('api/student_lessons_year', views.student_lessons_year),
    path('api/student_lessons_month', views.student_lessons_month),
    path('api/student_lessons_week', views.student_lessons_week),
    path('api/student_subjects_lessons', views.student_subjects_lessons),
]

