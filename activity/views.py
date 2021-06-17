from django.shortcuts import render
from student.models import Student
from django.contrib.auth.models import User
from .models import Lesson
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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