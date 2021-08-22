from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),

    path('login', views.login, name = 'manager_login'),
    path('password', views.password, name = 'manager_password'),
    path('logout', views.logout, name = 'manager_logout'),
    path('profile', views.profile, name = 'manager_profile'),

    path('employee/list', views.employee_list, name = 'manager_employee_list'),
    path('student/list', views.students_list, name = 'manager_student_list'),
    path('parent/list', views.parents_list, name = 'manager_parent_list'),

    path('request', views.req, name = 'manager_request'),
    path('request/list', views.req_list, name = 'manager_request_list'),

    path('highlights/student/<int:id>', views.highlights_student, name = "highlights_student"),
    path('highlights/employee/<int:id>', views.highlights_employee, name = "highlights_employee"),


    path('lessons', views.lessons, name = 'manager_lessons'),
    path('lessons/list', views.lessons_list, name = 'manager_lessons_list'),
    path('lesson/<int:id>', views.lesson, name = 'manager_lesson'),
    path('lesson/delete/<int:id>', views.lesson_delete, name = 'manager_lesson_delete'),
    path('lesson/edit/<int:id>', views.lesson_edit, name = 'manager_lesson_edit'),

    path('lesson/add', views.lesson_add, name = 'manager_lesson_add'),
    path('student/add', views.student_add, name = 'manager_student_add'),
    path('employee/add', views.employee_add, name = 'manager_employee_add'),
    path('parent/add', views.parent_add, name = 'manager_parent_add'),

    path('student/<int:id>', views.student, name = 'manager_student'),
    path('employee/<int:id>', views.employee, name = 'manager_employee'),
    path('parent/<int:id>', views.parent, name = 'manager_parent'),

]
