from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Corporation
from employee.models import Employee
from student.models import Student, Exam, Student
from activity.models import Lesson, Submission
from manager.models import Request
from bank.models import StudentAccount, StudentLessonBill

import re
import datetime


# login
# logout
# change password
# all students

# calendar
# list view lessons
# lesson open

# highlights


def validation_corporation(func):
     def validation(request, *args, **kwargs):
         try:
             corporation = Corporation.objects.get(user = request.user)
             return func(request, *args, **kwargs)
         except:
             auth.logout(request)
             return render(request, 'corporation/404.jinja')
     return validation

def index(request):
    context = {}
    if (request.user.is_authenticated):
        context['corporation'] = Corporation.objects.get(user = request.user)
        return redirect('corporation_highlights')
    else:
        return redirect('corporation_login')

def login(request):
    context = {}
    if (request.user.is_authenticated):
        return redirect('corporation_profile')

    if (request.method == 'POST'):
        if '@' in request.POST['login']:
            email = request.POST.get('login')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email = email)
            except:
                context['invalid'] = True
                return render(request, 'corporation/login.jinja', context)

            if (user.check_password(password)):
                auth.login(request, user)
                return redirect('corporation_profile')
            else:
                context['invalid'] = True
                return render(request, 'corporation/login.jinja', context)
        else:
            username = request.POST.get('login')
            password = request.POST.get('password')

            try:
                user = User.objects.get(username = username)
            except:
                context['invalid'] = True
                return render(request, 'corporation/login.jinja', context)

            if (user.check_password(password)):
                auth.login(request, user)
                return redirect('corporation_profile')
            else:
                context['invalid'] = True
                return render(request, 'corporation/login.jinja', context)

    return render(request, 'corporation/login.jinja', context)

def logout(request):
    context = {}
    context['corporation'] = Corporation.objects.get(user = request.user)
    auth.logout(request)
    return redirect('corporation_login')

@login_required
@validation_corporation
def password(request):
    context = {}
    context['corporation'] = Corporation.objects.get(user = request.user)
    if (request.method == 'POST'):
        context['wrong'] = ''
        old = request.POST['old_password']
        new = request.POST['password']
        repeat = request.POST['repeat_password']
        if (new != repeat):
            context['wrong']= 'passwords do not match'
            return render(request, 'corporation/password.jinja', context)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        # compiling regex
        pat = re.compile(reg)

        # searching regex
        mat = re.search(pat, new)
        if not mat:
            context['wrong'] = 'Password should have at least one number, one uppercase, one lowercase, one special symbol and must be between 6-20 characters long'
            return render(request, 'corporation/password.jinja', context)
        u = request.user
        if (u.check_password(old)):
            u.set_password(new)
            u.save()
            return redirect('corporation_login')
        else:
            # wrong password
            context['wrong']= 'Wrong Password'
            return render(request, 'corporation/password.jinja', context)

    return render(request, 'corporation/password.jinja', context)

@login_required
@validation_corporation
def highlights(request):
    context = {}
    context['corporation'] = Corporation.objects.get(user = request.user)
    student = Corporation.objects.get(user = request.user).child
    context['student'] = student
    context['lessons'] = lessons = [lesson for lesson in Lesson.objects.all() if (context['student'] in lesson.students.all())]
    context['classes'] = len(lessons)

    try:
        studentacc = StudentAccount.objects.get(student = student)
    except:
        studentacc = StudentAccount(student = student)
        studentacc.save()

    context['balance'] = studentacc.get_units_left()



    hrs = 0
    for lesson in lessons:
        diff = lesson.end-lesson.start
        hrs += diff.total_seconds()/3600
    context['hours'] = round(hrs, 2)

    return render(request, 'corporation/highlights.jinja', context)

@login_required
@validation_corporation
def req(request):
    context = {}
    context['corporation'] = Corporation.objects.get(user = request.user)
    if (request.method == 'POST'):
        req = request.POST['req']
        owner = request.user
        user_request = Request(owner = owner, description = req)
        user_request.save()

    return render(request, 'corporation/request.jinja', context)

@login_required
@validation_corporation
def lesson(request, id):
    context = {}
    l = Lesson.objects.get(id = id)
    context['lesson'] = l

    context['students_registered'] = l.students.all()

    context['homework_file'] = context['classwork_file'] = context['submission_file'] = False
    try:
        context['homework_file'] = l.homework.file
        context['classwork_file'] = l.classwork.file
    except:
        pass


    return render(request, 'corporation/lesson.jinja', context)

@login_required
@validation_corporation
def lessons(request):
    context = {}
    students = Corporation.objects.get(user = request.user).children
    context['lessons'] = {lesson for lesson in Lesson.objects.all() if (any(student in lesson.students.all() for student in lesson))}

    return render(request, 'corporation/lessons.jinja', context)

@login_required
@validation_corporation
def lessons_list(request):
    context = {}
    students = Corporation.objects.get(user = request.user).children
    context['lessons'] = {lesson for lesson in Lesson.objects.all() if (any(student in lesson.students.all() for student in lesson))}

    return render(request, 'corporation/lessons_list.jinja', context)

@login_required
@validation_corporation
def students(request):
    context = {}
    context['students'] = Corporation.objects.get(user = request.user).children
    return render(request, 'corporation/students.jinja', context)


@login_required
@validation_corporation
def student(request, id):
    context = {}
    context['corporation'] = Corporation.objects.get(user = request.user)
    context['student'] = student = Student.objects.get(id = id)
    context['interests'] = (student.interests or 'Education').split(',')
    context['languages'] = (student.languages or 'English').split(',')
    
    return render(request, 'corporation/student.jinja', context)
