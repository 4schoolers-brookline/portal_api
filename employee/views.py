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
            student.image = avatar
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
