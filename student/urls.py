from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'student_index'),
    path('login', views.login, name = 'student_login'),
    path('logout', views.logout, name = 'student_logout'),
    path('profile', views.profile, name = 'student_profile'),
    path('directory', views.directory, name = 'student_directory'),
]

