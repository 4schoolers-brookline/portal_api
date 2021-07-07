from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from student.models import Student, Exam
from django.contrib.auth.models import User
from activity.models import Lesson, Submission
from bank.models import StudentAccount, StudentLessonBill
import re
import datetime

def index(request):
    context = {}
    if (request.user.is_authenticated):
        context['employee'] = Employee.objects.get(user = request.user)
        return redirect('employee_highlights')
    else:
        return redirect('employee_login')

def login(request):
    # TODO: check if authenticated by other account type
    context = {}
    if (request.user.is_authenticated):
        return redirect('employee_profile')

    if (request.method == 'POST'):        
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except:
            context['invalid'] = True
            return render(request, 'employee/login.jinja', context)

        if (user.check_password(password)):
            auth.login(request, user)
            return redirect('employee_profile')
        else:
            context['invalid'] = True
            return render(request, 'employee/login.jinja', context)

    return render(request, 'employee/login.jinja', context)

@login_required
def logout(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    auth.logout(request)
    return redirect('employee_login')

@login_required
def profile(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    employee = Employee.objects.get(user = request.user)
    
    context['languages'] = employee.languages.split(',')
    context['interests'] = employee.interests.split(',')
    context['subjects'] = employee.subjects.split(',')

    if (request.method == 'POST'):
        if ('change_image' in request.POST):
            avatar = request.FILES['avatar']
            employee.image = avatar
            employee.save()
        else:
            employee.school = request.POST.get('school')
            graduation_year = int(request.POST.get('graduation_year'))
            employee.bio = request.POST.get('bio')
            employee.languages = request.POST.get('languages')
            employee.interests = request.POST.get('interests')
            employee.address = request.POST.get('address')
            employee.city = request.POST.get('city')
            employee.state = request.POST.get('state')
            employee.zip_code = request.POST.get('zip_code')
            employee.save()
        return redirect('employee_profile')
        
        

    return render(request, 'employee/profile.jinja', context)

@login_required
def password(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    if (request.method == 'POST'):
        context['wrong'] = ''
        old = request.POST['old_password']
        new = request.POST['password']
        repeat = request.POST['repeat_password']
        if (new != repeat):
            context['wrong']= 'passwords do not match'
            return render(request, 'employee/password.jinja', context)
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        # compiling regex
        pat = re.compile(reg)
        
        # searching regex                 
        mat = re.search(pat, new)
        if not mat:
            context['wrong'] = 'Password should have at least one number, one uppercase, one lowercase, one special symbol and must be between 6-20 characters long'
            return render(request, 'employee/password.jinja', context)
        u = request.user
        if (u.check_password(old)):
            u.set_password(new)
            u.save()
            return redirect('employee_login')
        else:
            # wrong password
            context['wrong']= 'Wrong Password'
            return render(request, 'employee/password.jinja', context)

    return render(request, 'employee/password.jinja', context)

@login_required
def student(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    context['student'] = Student.objects.get(id = id)
    context['interests'] = (context['student'].interests or 'Education').split(',')
    context['languages'] = (context['student'].languages or 'English').split(',')   
    
    return render(request, 'employee/student.jinja', context)

@login_required
def directory(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    context['students'] = Student.objects.all() # sorted(list(Employee.objects.all()), key = lambda x: x.priority)
    
    return render(request, 'employee/directory.jinja', context)

@login_required
def req(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    if (request.method == 'POST'):
        req = request.POST['req']

    return render(request, 'employee/request.jinja', context)

@login_required
def highlights(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)

    context['lessons'] = lessons = Lesson.objects.filter(teacher = context['employee'])
    context['classes'] = len(lessons)

    return render(request, 'employee/highlights.jinja', context)


@login_required
def lessons(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    return render(request, 'employee/lessons.jinja', context)

@login_required
def lessons_list(request):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    context['lessons'] = lessons = Lesson.objects.filter(teacher = context['employee'])
    return render(request, 'employee/lessons_list.jinja', context)

@login_required
def lesson(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
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
        return redirect('employee_lesson', l.id)

    return render(request, 'employee/lesson.jinja', context)


@login_required
def lesson_edit(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
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
            return render(request, 'employee/lesson_add.jinja', context)
                
        try:
            start_parsed = to_datetime(start)
            end_parsed = to_datetime(end)
        except:
            context['error'] = 'There was a problem with the selected time'
            return render(request, 'employee/lesson_add.jinja', context)

        lesson.name = name
        lesson.description = description
        lesson.teacher = t
        lesson.start = start_parsed
        lesson.end = end_parsed
        lesson.save()
        return redirect('employee_lessons')

    return render(request, 'employee/lesson_edit.jinja', context)

@login_required
def lesson_delete(request, id):
    context = {}
    context['employee'] = Employee.objects.get(user = request.user)
    lesson = context['lesson'] = Lesson.objects.get(pk = id)

    if (request.method == 'POST'):
        # TODO: Check if there is less than N hours before class
        lesson.delete()
        return redirect('employee_lessons')

    return render(request, 'employee/lesson_delete.jinja', context)


def to_datetime(s):
    date = s.split(' ')[0].split('/')
    time = s.split(' ')[1].split(':')
    x = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))

    return x