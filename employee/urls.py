from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name = 'employee_index'),

    path('login', views.login, name = 'employee_login'),
    path('password', views.password, name = 'employee_password'),
    path('logout', views.logout, name = 'employee_logout'),
    path('profile', views.profile, name = 'employee_profile'),

    path('highlights', views.highlights, name = 'employee_highlights'),
    path('directory', views.directory, name = 'employee_directory'),
    path('student/<int:id>', views.student, name = 'employee_student'),
    path('student/add', views.student_add, name = 'employee_student_add'),
    path('request', views.req, name = 'employee_request'),



    path('lessons', views.lessons, name = 'employee_lessons'),
    path('lessons/list', views.lessons_list, name = 'employee_lessons_list'),
    path('lesson/<int:id>', views.lesson, name = 'employee_lesson'),
    path('lesson/delete/<int:id>', views.lesson_delete, name = 'employee_lesson_delete'),
    path('lesson/edit/<int:id>', views.lesson_edit, name = 'employee_lesson_edit'),
    path('lesson/clone/<int:id>', views.lesson_clone, name = 'employee_lesson_clone'),

    path('lesson/add', views.lesson_add, name = 'employee_lesson_add'),

    # path('api/exams', views.student_exam_results_api),
]
