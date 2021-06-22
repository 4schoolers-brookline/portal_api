from django.shortcuts import render
from student.models import Student
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
            result[lesson.start.month-1] += 1
    return JsonResponse(result, safe = False)

@login_required
def student_lessons_month(request):
    student = Student.objects.get(user = request.user)
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]
    this_month = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
    days = [0 for _ in range(this_month+1)]
    for lesson in lessons:
        if (lesson.start.year == datetime.datetime.now().year and lesson.start.month == datetime.datetime.now().month):
            days[lesson.start.day-1] += 1
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
            result[lesson.start.weekday()] += 1


    return JsonResponse(result, safe = False)

@login_required
def student_subjects_lessons(request):
    student = Student.objects.get(user = request.user)
    lessons = [lesson for lesson in Lesson.objects.all() if (student in lesson.students.all())]

    result = {}

    for lesson in lessons:
        if (lesson.subject not in result.keys()):
            result[lesson.subject] = 1
        else:
            result[lesson.subject] += 1


    result_cleaned = {
        'subjects': [], 
        'lessons': []
    }

    for key, value in result.items():
        result_cleaned['subjects'].append(key)
        result_cleaned['lessons'].append(value)
    
    return JsonResponse(result_cleaned, safe = False)