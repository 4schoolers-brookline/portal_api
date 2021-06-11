from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from student.models import Student
from django.contrib.auth.models import User
from activity.models import Lesson, Submission
import re

def index(request):
    if (request.user.is_authenticated):
        return redirect('student_profile')
    else:
        context['student'] = Student.objects.get(user = request.user)
        return redirect('student_login')
    

@login_required
def lesson_add(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['employees'] = Employee.objects.all()

    if (request.method == 'POST'):
        name = request.POST['name']
        subject = request.POST['subject']
        teacher = request.POST['teacher']
        description = request.POST['descr']
        start = request.POST['']
        end = request.POST['']

        lesson = Lesson(name = name, subject = subject, description = description, teacher = teacher, start = start, end=end)

        lesson.students.add(context['student'])



 
    return render(request, 'student/lesson_add.jinja', context)

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
    context['test'] = 'loool'
    return render(request, 'student/lessons.jinja', context)


@login_required
def directory(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['employees'] = sorted(list(Employee.objects.all()), key = lambda x: x.priority)
    
    return render(request, 'student/directory.jinja', context)

@login_required
def profile(request):
    context = {}
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
    context['interests'] = context['employee'].interests.split(',')
    context['languages'] = context['employee'].languages.split(',')   
    context['subjects'] = context['employee'].subjects.split(',')   

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

