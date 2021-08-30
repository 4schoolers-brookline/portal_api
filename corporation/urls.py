from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),

    path('login', views.login, name = 'corporation_login'),
    path('password', views.password, name = 'corporation_password'),
    path('logout', views.logout, name = 'corporation_logout'),
    path('highlights', views.highlights, name = 'corporation_highlights'),
    

    path('students', views.students, name = 'corporation_student_list'),
    
    path('lessons', views.lessons, name = 'corporation_lessons'),
    path('lessons/list', views.lessons_list, name = 'corporation_lessons_list'),
    
    path('student/<int:id>', views.student, name = 'corporation_student'),
    
]
