from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Parent
from employee.models import Employee
from student.models import Student, Exam, Student
from activity.models import Lesson, Submission
from manager.models import Request
from bank.models import StudentAccount, StudentLessonBill

import re
import datetime


def validation_parent(func):

     def validation(request, *args, **kwargs):
         try:
             parent = Parent.objects.get(user = request.user)
             return func(request, *args, **kwargs)
         except:
             return render(request, 'parent/404.jinja')
     return validation


def index(request):
    context = {}
    if (request.user.is_authenticated):
        context['parent'] = Parent.objects.get(user = request.user)
        return redirect('parent_highlights')
    else:
        return redirect('parent_login')


@login_required
@validation_parent
def student_exam_results_api(request):
    student = Parent.objects.get(user = request.user).child
    exams = Exam.objects.filter(taker = student)
    names = [exam.name for exam in exams]
    percents = [exam.percentage for exam in exams]




    if ('Regular SAT Math' not in names):
        names.append('Regular SAT Math')
        percents.append(0)
    if ('Regular SAT English' not in names):
        names.append('Regular SAT English')
        percents.append(0)
    if ('ACT Math' not in names):
        names.append('ACT Math')
        percents.append(0)
    if ('ACT English' not in names):
        names.append('ACT English')
        percents.append(0)
    if ('ACT Science' not in names):
        names.append('ACT Science')
        percents.append(0)

    result = {
        'exams': names,
        'percentages': percents,
    }
    return JsonResponse(result, safe = False)

def login(request):
    # TODO: check if authenticated by other account type
    context = {}
    if (request.user.is_authenticated):
        return redirect('parent_profile')

    if (request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            context['invalid'] = True
            return render(request, 'parent/login.jinja', context)

        if (user.check_password(password)):
            auth.login(request, user)
            return redirect('parent_profile')
        else:
            context['invalid'] = True
            return render(request, 'parent/login.jinja', context)

    return render(request, 'parent/login.jinja', context)

def logout(request):
    context = {}
    context['parent'] = Parent.objects.get(user = request.user)
    auth.logout(request)
    return redirect('parent_login')

@login_required
@validation_parent
def password(request):
    context = {}
    context['parent'] = Parent.objects.get(user = request.user)
    if (request.method == 'POST'):
        context['wrong'] = ''
        old = request.POST['old_password']
        new = request.POST['password']
        repeat = request.POST['repeat_password']
        if (new != repeat):
            context['wrong']= 'passwords do not match'
            return render(request, 'parent/password.jinja', context)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        # compiling regex
        pat = re.compile(reg)

        # searching regex
        mat = re.search(pat, new)
        if not mat:
            context['wrong'] = 'Password should have at least one number, one uppercase, one lowercase, one special symbol and must be between 6-20 characters long'
            return render(request, 'parent/password.jinja', context)
        u = request.user
        if (u.check_password(old)):
            u.set_password(new)
            u.save()
            return redirect('parent_login')
        else:
            # wrong password
            context['wrong']= 'Wrong Password'
            return render(request, 'parent/password.jinja', context)

    return render(request, 'parent/password.jinja', context)

@login_required
@validation_parent
def profile(request):
    context = {}
    student = Parent.objects.get(user = request.user).child
    context['parent'] = Parent.objects.get(user = request.user)
    parent = Parent.objects.get(user = request.user)

    if (request.method == 'POST'):
        if ('change_image' in request.POST):
            avatar = request.FILES['avatar']
            parent.image = avatar
            parent.save()
        else:
            parent.phone = request.POST['phone']
            parent.save()
        return redirect('parent_profile')

    return render(request, 'parent/profile.jinja', context)

@login_required
@validation_parent
def highlights(request):
    context = {}
    context['parent'] = Parent.objects.get(user = request.user)
    student = Parent.objects.get(user = request.user).child
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

    return render(request, 'parent/highlights.jinja', context)

@login_required
@validation_parent
def req(request):
    context = {}
    context['parent'] = Parent.objects.get(user = request.user)
    if (request.method == 'POST'):
        req = request.POST['req']
        owner = request.user
        user_request = Request(owner = owner, description = req)
        user_request.save()

    return render(request, 'parent/request.jinja', context)

@login_required
@validation_parent
def lesson(request, id):
    context = {}
    context['student'] = Parent.objects.get(user = request.user).child
    l = Lesson.objects.get(id = id)
    context['lesson'] = l
    context['students_registered'] = l.students.all()

    try:
        submission = l.homework_submissions.all().get(owner = request.user)
    except:
        submission = None

    context['submission'] = submission

    context['homework_file'] = context['classwork_file'] = context['submission_file'] = False
    try:
        context['homework_file'] = l.homework.file
    except:
        pass
    try:
        context['classwork_file'] = l.classwork.file
    except:
        pass
    try:
        context['submission_file'] = submission.file
    except:
        pass

    if (request.method == 'POST'):
        description = request.POST['descr']
        try:
            uploaded_file = request.FILES['subm']

            subm = Submission(name = 'lesson{}'.format(l.pk), description = description, owner = request.user, type = 'Homework_Submission', file = uploaded_file, account_type = 'student')
        except:
            subm = Submission(name = 'lesson{}'.format(l.pk), description = description, owner = request.user, type = 'Homework_Submission', account_type = 'student')
        subm.save()

        l.homework_submissions.add(subm)
        l.save()
        return redirect('student_lesson', l.id)

    return render(request, 'parent/lesson.jinja', context)

@login_required
@validation_parent
def lessons(request):
    context = {}
    context['student'] = Parent.objects.get(user = request.user).child

    return render(request, 'parent/lessons.jinja', context)

@login_required
@validation_parent
def lessons_list(request):
    context = {}
    context['student'] = Parent.objects.get(user = request.user).child
    context['lessons'] = [lesson for lesson in Lesson.objects.all() if (context['student'] in lesson.students.all())]

    return render(request, 'parent/lessons_list.jinja', context)

@login_required
@validation_parent
def directory(request):
    context = {}
    context['parent'] = Parent.objects.get(user = request.user)
    context['employees'] = sorted(list(Employee.objects.all()), key = lambda x: x.priority)

    return render(request, 'parent/directory.jinja', context)

@login_required
@validation_parent
def employee(request, id):
    context = {}
    context['parent'] = Parent.objects.get(user = request.user)
    context['employee'] = Employee.objects.get(id = id)
    context['interests'] = (context['employee'].interests or 'Education').split(',')
    context['languages'] = (context['employee'].languages or 'English').split(',')
    context['subjects'] = (context['employee'].subjects or 'Advising').split(',')

    return render(request, 'parent/employee.jinja', context)

@login_required
@validation_parent
def student(request, id):
    context = {}
    context['parent'] = Parent.objects.get(user = request.user)
    context['student'] = Student.objects.get(id = id)
    context['interests'] = (context['student'].interests or 'Education').split(',')
    context['languages'] = (context['student'].languages or 'English').split(',')

    return render(request, 'parent/student.jinja', context)
