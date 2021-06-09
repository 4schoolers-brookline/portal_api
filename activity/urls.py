from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('api/student_lessons', views.student_lessons),
]

