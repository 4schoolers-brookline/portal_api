from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),

    path('login', views.login, name = 'parent_login'),
    path('logout', views.logout, name = 'parent_logout'),
    path('password', views.password, name = 'parent_password'),

    path('profile', views.profile, name = 'parent_profile'),
    path('highlights', views.highlights, name = 'parent_highlights'),

    path('directory', views.directory, name = 'parent_directory'),
    path('highlights', views.highlights, name = 'parent_highlights'),
    path('request', views.req, name = 'parent_request'),

    path('lessons', views.lessons, name = 'parent_lessons'),
    path('lessons/list', views.lessons_list, name = 'parent_lessons_list'),
    path('lesson/<int:id>', views.lesson, name = 'parent_lesson'),

    path('employee/<int:id>', views.employee, name = 'parent_employee'),
    path('student/<int:id>', views.student, name = 'parent_student'),

    path('api/exams', views.student_exam_results_api),
]
