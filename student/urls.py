from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name = 'student_index'),

    path('login', views.login, name = 'student_login'),
    path('logout', views.logout, name = 'student_logout'),
    path('password', views.password, name = 'student_password'),

    path('profile', views.profile, name = 'student_profile'),
    path('directory', views.directory, name = 'student_directory'),
    path('highlights', views.highlights, name = 'student_highlights'),
    path('request', views.req, name = 'student_request'),

    path('lessons', views.lessons, name = 'student_lessons'),
    path('lessons/list', views.lessons_list, name = 'student_lessons_list'),
    path('lesson/<int:id>', views.lesson, name = 'student_lesson'),
    path('lesson/add', views.lesson_add, name = 'student_lesson_add'),
    path('lesson/delete/<int:id>', views.lesson_delete, name = 'student_lesson_delete'),
    path('lesson/edit/<int:id>', views.lesson_edit, name = 'student_lesson_edit'),
    path('employee/<int:id>', views.employee, name = 'student_employee'),

    path('api/exams', views.student_exam_results_api),
]
