from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from student.models import Student
from django.contrib.auth.models import User
from activity.models import Lesson

def index(request):
    if (request.user.is_authenticated):
        return redirect('student_profile')
    else:
        context['student'] = Student.objects.get(user = request.user)
        return redirect('student_login')
    
@login_required
def password(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['employees'] = Employee.objects.all()
    return render(request, 'student/change_password.jinja', context)


@login_required
def lesson_add(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    context['test'] = 'loool'
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
    context['student'] = Student.objects.get(user = request.user)
    context['employees'] = Employee.objects.all()
    return render(request, 'student/directory.jinja', context)

@login_required
def profile(request):
    context = {}
    context['student'] = Student.objects.get(user = request.user)
    student = Student.objects.get(user = request.user)
    
    context['languages'] = student.languages.split(',')
    context['interests'] = student.interests.split(',')

    if (request.method == 'POST'):
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
    return redirect('student_login')





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

