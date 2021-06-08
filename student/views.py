from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from employee.models import Employee
from student.models import Student
from django.contrib.auth.models import User

def index(request):
    if (request.user.is_authenticated):
        return redirect('student_profile')
    else:
        return redirect('student_login')
    
    


@login_required
def directory(request):
    context = {}
    context['employees'] = Employee.objects.all()
    return render(request, 'student/directory.jinja', context)

@login_required
def profile(request):
    context = {}
    student = Student.objects.get(user = request.user)
    context['student'] = student
    return render(request, 'student/profile.jinja', context)

@login_required
def logout(request):
    context = {}
    auth.logout(request)
    return redirect('student_login')





def login(request):
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


