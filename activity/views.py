from django.shortcuts import render
from student.models import Student
from employee.models import Employee
from parent.models import Parent
from manager.models import Manager
from corporation.models import Corporation

from django.contrib.auth.models import User
from .models import Lesson
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import datetime
from calendar import monthrange

def index(request):
    return 'Hello activity'




@login_required
def student_lessons(request):
    student = Student.objects.get(user = request.user)
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    url = lambda x: 'lesson/'+str(x)
    result = [
        {
            'title': lesson.name,
            'start': lesson.start,
            'end': lesson.end,
            'url': url(lesson.pk),
        }
        for lesson in lessons
    ]

    return JsonResponse(result, safe = False)

@login_required
def student_lessons_year(request):
    student = Student.objects.get(user = request.user)
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    result = [0 for _ in range(13)]
    for lesson in lessons:
        if lesson.start.year == datetime.datetime.now().year:
            result[lesson.start.month-1] += (lesson.end-lesson.start).total_seconds()/3600
    return JsonResponse(result, safe = False)

@login_required
def student_lessons_month(request):
    student = Student.objects.get(user = request.user)
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    this_month = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
    days = [0 for _ in range(this_month+1)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month):
            days[lesson.start.day-1] += (lesson.end-lesson.start).total_seconds()/3600
    result = {
        'total': [i for i in range(1,this_month+1)],
        'days': days
    }

    return JsonResponse(result, safe = False)

@login_required
def student_lessons_week(request):
    student = Student.objects.get(user = request.user)
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    result = [0 for _ in range(8)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month and lesson.start.isocalendar()[1]==datetime.datetime.now().isocalendar()[1]):
            result[lesson.start.weekday()] += (lesson.end-lesson.start).total_seconds()/3600


    return JsonResponse(result, safe = False)

@login_required
def student_subjects_lessons(request):
    student = Student.objects.get(user = request.user)
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]

    result = {}

    for lesson in lessons:
        if (lesson.subject not in result.keys()):
            result[lesson.subject] = (lesson.end-lesson.start).total_seconds()/3600
        else:
            result[lesson.subject] += (lesson.end-lesson.start).total_seconds()/3600


    result_cleaned = {
        'subjects': [],
        'lessons': []
    }

    for key, value in result.items():
        result_cleaned['subjects'].append(key)
        result_cleaned['lessons'].append(value)

    return JsonResponse(result_cleaned, safe = False)

@login_required
def employee_lessons(request):
    employee = Employee.objects.get(user = request.user)
    lessons = Lesson.objects.filter(teacher = employee)
    url = lambda x: 'lesson/'+str(x)
    result = [
        {
            'title': lesson.name,
            'start': lesson.start,
            'end': lesson.end,
            'url': url(lesson.pk),
        }
        for lesson in lessons
    ]

    return JsonResponse(result, safe = False)

@login_required
def employee_lessons_week(request):
    employee = Employee.objects.get(user = request.user)
    lessons = Lesson.objects.filter(teacher = employee)
    result = [0 for _ in range(8)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month and lesson.start.isocalendar()[1]==datetime.datetime.now().isocalendar()[1]):
            result[lesson.start.weekday()] += (lesson.end-lesson.start).total_seconds()/3600


    return JsonResponse(result, safe = False)

@login_required
def employee_lessons_month(request):
    employee = Employee.objects.get(user = request.user)
    lessons = Lesson.objects.filter(teacher = employee)
    this_month = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
    days = [0 for _ in range(this_month+1)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month):
            days[lesson.start.day-1] += (lesson.end-lesson.start).total_seconds()/3600
    result = {
        'total': [i for i in range(1,this_month+1)],
        'days': days
    }

    return JsonResponse(result, safe = False)

@login_required
def employee_lessons_year(request):
    employee = Employee.objects.get(user = request.user)
    lessons = Lesson.objects.filter(teacher = employee)
    result = [0 for _ in range(13)]
    for lesson in lessons:
        if lesson.start.year == datetime.datetime.now().year:
            result[lesson.start.month-1] += (lesson.end-lesson.start).total_seconds()/3600
    return JsonResponse(result, safe = False)

@login_required
def employee_subjects_lessons(request):
    employee = Employee.objects.get(user = request.user)
    lessons = Lesson.objects.filter(teacher = employee)

    result = {}

    for lesson in lessons:
        if (lesson.subject not in result.keys()):
            result[lesson.subject] = (lesson.end-lesson.start).total_seconds()/3600
        else:
            result[lesson.subject] += (lesson.end-lesson.start).total_seconds()/3600


    result_cleaned = {
        'subjects': [],
        'lessons': []
    }

    for key, value in result.items():
        result_cleaned['subjects'].append(key)
        result_cleaned['lessons'].append(value)

    return JsonResponse(result_cleaned, safe = False)

@login_required
def parent_lessons(request):
    student = Parent.objects.get(user = request.user).child
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    url = lambda x: 'lesson/'+str(x)
    result = [
        {
            'title': lesson.name,
            'start': lesson.start,
            'end': lesson.end,
            'url': url(lesson.pk),
        }
        for lesson in lessons
    ]

    return JsonResponse(result, safe = False)

@login_required
def parent_lessons_year(request):
    student = Parent.objects.get(user = request.user).child
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    result = [0 for _ in range(13)]
    for lesson in lessons:
        if lesson.start.year == datetime.datetime.now().year:
            result[lesson.start.month-1] += (lesson.end-lesson.start).total_seconds()/3600
    return JsonResponse(result, safe = False)

@login_required
def parent_lessons_month(request):
    student = Parent.objects.get(user = request.user).child
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    this_month = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
    days = [0 for _ in range(this_month+1)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month):
            days[lesson.start.day-1] += (lesson.end-lesson.start).total_seconds()/3600
    result = {
        'total': [i for i in range(1,this_month+1)],
        'days': days
    }

    return JsonResponse(result, safe = False)

@login_required
def parent_lessons_week(request):
    student = Parent.objects.get(user = request.user).child
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    result = [0 for _ in range(8)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month and lesson.start.isocalendar()[1]==datetime.datetime.now().isocalendar()[1]):
            result[lesson.start.weekday()] += (lesson.end-lesson.start).total_seconds()/3600


    return JsonResponse(result, safe = False)

@login_required
def parent_subjects_lessons(request):
    student = Parent.objects.get(user = request.user).child
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]

    result = {}

    for lesson in lessons:
        if (lesson.subject not in result.keys()):
            result[lesson.subject] = (lesson.end-lesson.start).total_seconds()/3600
        else:
            result[lesson.subject] += (lesson.end-lesson.start).total_seconds()/3600


    result_cleaned = {
        'subjects': [],
        'lessons': []
    }

    for key, value in result.items():
        result_cleaned['subjects'].append(key)
        result_cleaned['lessons'].append(value)

    return JsonResponse(result_cleaned, safe = False)

@login_required
def manager_lessons(request):
    manager = Manager.objects.get(user = request.user)
    result = []
    for student in manager.students.all():
        lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
        url = lambda x: 'lesson/'+str(x)
        result += [
            {
                'title': lesson.name,
                'start': lesson.start,
                'end': lesson.end,
                'url': url(lesson.pk),
            }
            for lesson in lessons if lesson not in result
        ]
    for employee in manager.employees.all():
        lessons = Lesson.objects.filter(teacher = employee)
        url = lambda x: 'lesson/'+str(x)
        result += [
            {
                'title': lesson.name,
                'start': lesson.start,
                'end': lesson.end,
                'url': url(lesson.pk),
            }
            for lesson in lessons
        ]
    final_result = []
    for lesson in result:
        if lesson not in final_result:
            final_result.append(lesson)
    return JsonResponse(final_result, safe = False)

@login_required
def manager_student_lessons(request):
    student = Student.objects.get(id = request.GET['student_id'])
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    url = lambda x: 'lesson/'+str(x)
    result = [
        {
            'title': lesson.name,
            'start': lesson.start,
            'end': lesson.end,
            'url': url(lesson.pk),
        }
        for lesson in lessons
    ]

    return JsonResponse(result, safe = False)

@login_required
def manager_student_lessons_year(request):
    student = Student.objects.get(id = request.GET['student_id'])
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    result = [0 for _ in range(13)]
    for lesson in lessons:
        if lesson.start.year == datetime.datetime.now().year:
            result[lesson.start.month-1] += (lesson.end-lesson.start).total_seconds()/3600
    return JsonResponse(result, safe = False)

@login_required
def manager_student_lessons_month(request):
    student = Student.objects.get(id = request.GET['student_id'])
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    this_month = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
    days = [0 for _ in range(this_month+1)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month):
            days[lesson.start.day-1] += (lesson.end-lesson.start).total_seconds()/3600
    result = {
        'total': [i for i in range(1,this_month+1)],
        'days': days
    }

    return JsonResponse(result, safe = False)

@login_required
def manager_student_lessons_week(request):
    student = Student.objects.get(id = request.GET['student_id'])
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    result = [0 for _ in range(8)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month and lesson.start.isocalendar()[1]==datetime.datetime.now().isocalendar()[1]):
            result[lesson.start.weekday()] += (lesson.end-lesson.start).total_seconds()/3600


    return JsonResponse(result, safe = False)

@login_required
def manager_student_subjects_lessons(request):
    student = Student.objects.get(id = request.GET['student_id'])
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]

    result = {}

    for lesson in lessons:
        if (lesson.subject not in result.keys()):
            result[lesson.subject] = (lesson.end-lesson.start).total_seconds()/3600
        else:
            result[lesson.subject] += (lesson.end-lesson.start).total_seconds()/3600


    result_cleaned = {
        'subjects': [],
        'lessons': []
    }

    for key, value in result.items():
        result_cleaned['subjects'].append(key)
        result_cleaned['lessons'].append(value)

    return JsonResponse(result_cleaned, safe = False)

@login_required
def manager_employee_lessons(request):
    employee = Employee.objects.get(id = request.GET['employee_id'])
    lessons = Lesson.objects.filter(teacher = employee)
    url = lambda x: 'lesson/'+str(x)
    result = [
        {
            'title': lesson.name,
            'start': lesson.start,
            'end': lesson.end,
            'url': url(lesson.pk),
        }
        for lesson in lessons
    ]

    return JsonResponse(result, safe = False)

@login_required
def manager_employee_lessons_week(request):
    employee = Employee.objects.get(id = request.GET['employee_id'])
    lessons = Lesson.objects.filter(teacher = employee)
    result = [0 for _ in range(8)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month and lesson.start.isocalendar()[1]==datetime.datetime.now().isocalendar()[1]):
            result[lesson.start.weekday()] += (lesson.end-lesson.start).total_seconds()/3600


    return JsonResponse(result, safe = False)

@login_required
def manager_employee_lessons_month(request):
    employee = Employee.objects.get(id = request.GET['employee_id'])
    lessons = Lesson.objects.filter(teacher = employee)
    this_month = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
    days = [0 for _ in range(this_month+1)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month):
            days[lesson.start.day-1] += (lesson.end-lesson.start).total_seconds()/3600
    result = {
        'total': [i for i in range(1,this_month+1)],
        'days': days
    }

    return JsonResponse(result, safe = False)

@login_required
def manager_employee_lessons_year(request):

    employee = Employee.objects.get(id = request.GET['employee_id'])
    lessons = Lesson.objects.filter(teacher = employee)
    result = [0 for _ in range(13)]
    for lesson in lessons:
        if lesson.start.year == datetime.datetime.now().year:
            result[lesson.start.month-1] += (lesson.end-lesson.start).total_seconds()/3600
    return JsonResponse(result, safe = False)

@login_required
def manager_employee_subjects_lessons(request):
    employee = Employee.objects.get(id = request.GET['employee_id'])
    lessons = Lesson.objects.filter(teacher = employee)

    result = {}

    for lesson in lessons:
        if (lesson.subject not in result.keys()):
            result[lesson.subject] = (lesson.end-lesson.start).total_seconds()/3600
        else:
            result[lesson.subject] += (lesson.end-lesson.start).total_seconds()/3600


    result_cleaned = {
        'subjects': [],
        'lessons': []
    }

    for key, value in result.items():
        result_cleaned['subjects'].append(key)
        result_cleaned['lessons'].append(value)

    return JsonResponse(result_cleaned, safe = False)



@login_required
def corporation_lessons_week(request):

    students = Corporation.objects.get(user = request.user).children.all()
    lessons = list({lesson for lesson in Lesson.objects.all() if (any(student in lesson.students.all() for student in students))})
    result = [0 for _ in range(8)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month and lesson.start.isocalendar()[1]==datetime.datetime.now().isocalendar()[1]):
            result[lesson.start.weekday()] += (lesson.end-lesson.start).total_seconds()/3600


    return JsonResponse(result, safe = False)

@login_required
def corporation_lessons_month(request):
    students = Corporation.objects.get(user = request.user).children.all()
    lessons = list({lesson for lesson in Lesson.objects.all() if (any(student in lesson.students.all() for student in students))})
    this_month = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
    days = [0 for _ in range(this_month+1)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month):
            days[lesson.start.day-1] += (lesson.end-lesson.start).total_seconds()/3600
    result = {
        'total': [i for i in range(1,this_month+1)],
        'days': days
    }

    return JsonResponse(result, safe = False)

@login_required
def corporation_lessons_year(request):

    students = Corporation.objects.get(user = request.user).children.all()
    lessons = list({lesson for lesson in Lesson.objects.all() if (any(student in lesson.students.all() for student in students))})
    result = [0 for _ in range(13)]
    for lesson in lessons:
        if lesson.start.year == datetime.datetime.now().year:
            result[lesson.start.month-1] += (lesson.end-lesson.start).total_seconds()/3600
    return JsonResponse(result, safe = False)

@login_required
def corporation_subjects_lessons(request):
    students = Corporation.objects.get(user = request.user).children.all()
    lessons = list({lesson for lesson in Lesson.objects.all() if (any(student in lesson.students.all() for student in students))})
    
    result = {}

    for lesson in lessons:
        if (lesson.subject not in result.keys()):
            result[lesson.subject] = (lesson.end-lesson.start).total_seconds()/3600
        else:
            result[lesson.subject] += (lesson.end-lesson.start).total_seconds()/3600


    result_cleaned = {
        'subjects': [],
        'lessons': []
    }

    for key, value in result.items():
        result_cleaned['subjects'].append(key)
        result_cleaned['lessons'].append(value)

    return JsonResponse(result_cleaned, safe = False)

@login_required
def corporation_students_lessons(request):
    students = Corporation.objects.get(user = request.user).children.all()
    lessons = list({lesson for lesson in Lesson.objects.all() if (any(student in lesson.students.all() for student in students))})
    


    result = {}

    for lesson in lessons:
        studs = lesson.students.all()
        for s in studs:
            if (s.user.username in result.keys()):
                result[s.user.username] += (lesson.end-lesson.start).total_seconds()/3600
            else:
                result[s.user.username] = (lesson.end-lesson.start).total_seconds()/3600



    result_cleaned = {
        'students': [],
        'lessons': []
    }

    for key, value in result.items():
        result_cleaned['students'].append(key)
        result_cleaned['lessons'].append(value)

    return JsonResponse(result_cleaned, safe = False)

def corporation_lessons(request):
    students = Corporation.objects.get(user = request.user).children.all()
    lessons = list({lesson for lesson in Lesson.objects.all() if (any(student in lesson.students.all() for student in students))})
    
    url = lambda x: 'lesson/'+str(x)
    result = [
        {
            'title': lesson.name,
            'start': lesson.start,
            'end': lesson.end,
            'url': url(lesson.pk),
        }
        for lesson in lessons
    ]

    return JsonResponse(result, safe = False)
