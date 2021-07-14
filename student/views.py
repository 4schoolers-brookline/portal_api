from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from employee.models import Employee
from student.models import Student, Exam
from activity.models import Lesson, Submission
from bank.models import StudentAccount, StudentLessonBill

import re
import datetime

def index(request):
    context = {}
    if (request.user.is_authenticated):
        context['student'] = Student.objects.get(user = request.user)
        return redirect('student_highlights')
    else:
        return redirect('student_login')


@login_required
def student_exam_results_api(request):
    student = Student.objects.get(user = request.user)
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


@login_required
def highlights(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['lessons'] = lessons = [lesson for lesson in Lesson.objects.all() if (context['student'] in lesson.students.all())]
    context['classes'] = len(lessons)

    try:
        studentacc = StudentAccount.objects.get(student = Student.objects.get(user = request.user))
    except:
        studentacc = StudentAccount(student = Student.objects.get(user = request.user))
        studentacc.save()

    context['balance'] = studentacc.get_units_left()



    hrs = 0
    for lesson in lessons:
        diff = lesson.end-lesson.start
        hrs += diff.total_seconds()/3600
    context['hours'] = round(hrs, 2)

    return render(request, 'student/highlights.jinja', context)

@login_required
def req(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    if (request.method == 'POST'):
        req = request.POST['req']

    return render(request, 'student/request.jinja', context)

@login_required
def lesson_add(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['employees'] = sorted(list(Employee.objects.all()), key = lambda x: -x.priority)

    if (request.method == 'POST'):
        name = request.POST['name']
        subject = request.POST['subject']
        teacher = request.POST['teacher']
        description = request.POST['descr']
        start = request.POST['start']
        end = request.POST['end']

        try:
            t = Employee.objects.get(pk = teacher)
        except:
            context['error'] = 'Teacher does not exist'
            return render(request, 'student/lesson_add.jinja', context)

        try:
            start_parsed = to_datetime(start)
            end_parsed = to_datetime(end)
        except:
            context['error'] = 'There was a problem with the selected time'
            return render(request, 'student/lesson_add.jinja', context)

        lesson = Lesson(name = name, subject = subject, description = description, teacher = t, start = start_parsed, end = end_parsed)
        lesson.save()
        lesson.students.add(context['student'])
        lesson.save()

        return redirect('student_lessons')

    return render(request, 'student/lesson_add.jinja', context)


@login_required
def lesson_edit(request, id):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    lesson = context['lesson'] = Lesson.objects.get(pk = id)
    context['employees'] = sorted(list(Employee.objects.all()), key = lambda x: x.priority)

    if (request.method == 'POST'):
        name = request.POST['name']
        subject = request.POST['subject']
        teacher = request.POST['teacher']
        description = request.POST['descr']
        start = request.POST['start']
        end = request.POST['end']

        try:
            t = Employee.objects.get(pk = teacher)
        except:
            context['error'] = 'Teacher does not exist'
            return render(request, 'student/lesson_edit.jinja', context)

        try:
            start_parsed = to_datetime(start)
            end_parsed = to_datetime(end)
        except:
            context['error'] = 'There was a problem with the selected time'
            return render(request, 'student/lesson_edit.jinja', context)

        lesson.name = name
        lesson.description = description
        lesson.teacher = t
        lesson.start = start_parsed
        lesson.end = end_parsed
        lesson.save()
        return redirect('student_lessons')

    return render(request, 'student/lesson_edit.jinja', context)

@login_required
def lesson_delete(request, id):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    lesson = context['lesson'] = Lesson.objects.get(pk = id)

    if (request.method == 'POST'):
        # TODO: Check if there is less than N hours before class
        lesson.delete()
        return redirect('student_lessons')

    return render(request, 'student/lesson_delete.jinja', context)


def to_datetime(s):
    date = s.split(' ')[0].split('/')
    time = s.split(' ')[1].split(':')
    x = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))

    return x


@login_required
def lesson(request, id):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
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

    return render(request, 'student/lesson.jinja', context)

@login_required
def lessons(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    return render(request, 'student/lessons.jinja', context)

@login_required
def lessons_list(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['lessons'] = [lesson for lesson in Lesson.objects.all() if (context['student'] in lesson.students.all())]
    return render(request, 'student/lessons_list.jinja', context)

@login_required
def directory(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['employees'] = sorted(list(Employee.objects.all()), key = lambda x: x.priority)

    return render(request, 'student/directory.jinja', context)

@login_required
def profile(request):
    context = {}
    print(Student.objects.all())
    context['student'] = Student.objects.get(user = request.user)
    student = Student.objects.get(user = request.user)

    context['languages'] = student.languages.split(',')
    context['interests'] = student.interests.split(',')

    if (request.method == 'POST'):
        if ('change_image' in request.POST):
            avatar = request.FILES['avatar']
            student.image = avatar
            student.save()
        else:
            student.school = request.POST.get('school')
            graduation_year = int(request.POST.get('graduation_year'))
            student.bio = request.POST.get('bio')
            student.languages = request.POST.get('languages')
            student.interests = request.POST.get('interests')
            student.address = request.POST.get('address')
            student.city = request.POST.get('city')
            student.state = request.POST.get('state')
            student.zip_code = request.POST.get('zip_code')
            student.save()
        return redirect('student_profile')



    return render(request, 'student/profile.jinja', context)

@login_required
def logout(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    auth.logout(request)
    return redirect('student_login')

@login_required
def employee(request, id):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['employee'] = Employee.objects.get(id = id)
    context['interests'] = (context['employee'].interests or 'Education').split(',')
    context['languages'] = (context['employee'].languages or 'English').split(',')
    context['subjects'] = (context['employee'].subjects or 'Advising').split(',')

    return render(request, 'student/employee.jinja', context)

def error_404(request, exception):
    context = {}
    return render(request,'student/404.jinja', context)
def error_500(request, exception):
    context = {}
    return render(request,'student/404.jinja', context)

@login_required
def password(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    if (request.method == 'POST'):
        context['wrong'] = ''
        old = request.POST['old_password']
        new = request.POST['password']
        repeat = request.POST['repeat_password']
        if (new != repeat):
            context['wrong']= 'passwords do not match'
            return render(request, 'student/password.jinja', context)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        # compiling regex
        pat = re.compile(reg)

        # searching regex
        mat = re.search(pat, new)
        if not mat:
            context['wrong'] = 'Password should have at least one number, one uppercase, one lowercase, one special symbol and must be between 6-20 characters long'
            return render(request, 'student/password.jinja', context)
        u = request.user
        if (u.check_password(old)):
            u.set_password(new)
            u.save()
            return redirect('student_login')
        else:
            # wrong password
            context['wrong']= 'Wrong Password'
            return render(request, 'student/password.jinja', context)

    return render(request, 'student/password.jinja', context)

def login(request):
    # TODO: check if authenticated by other account type
    context = {}
    if (request.user.is_authenticated):
        return redirect('student_profile')

    if (request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            context['invalid'] = True
            return render(request, 'student/login.jinja', context)

        if (user.check_password(password)):
            auth.login(request, user)
            return redirect('student_profile')
        else:
            context['invalid'] = True
            return render(request, 'student/login.jinja', context)

    return render(request, 'student/login.jinja', context)
