from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name = 'student_index'),
    path('login', views.login, name = 'student_login'),
    path('logout', views.logout, name = 'student_logout'),
    path('profile', views.profile, name = 'student_profile'),
    path('directory', views.directory, name = 'student_directory'),
    path('password', views.password, name = 'student_password'),
    path('lessons', views.lessons, name = 'student_lessons'),
    path('lesson/<int:id>', views.lesson, name = 'student_lesson'),
    path('lesson/add', views.lesson_add, name = 'student_lesson_add'),
    path('employee/<int:id>', views.employee, name = 'student_employee'),
]


