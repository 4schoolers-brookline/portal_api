from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from parent.models import Parent
from manager.models import Manager
from employee.models import Employee
from student.models import Student

def index(request):
    context = {}
    if (request.user.is_authenticated):
        try:
            context['employee'] = Employee.objects.get(user = request.user)
            return redirect('employee_login')
        except:
            pass
        try:
            context['student'] = Student.objects.get(user = request.user)
            return redirect('student_login')
        except:
            pass
        try:
            context['parent'] = Parent.objects.get(user = request.user)
            return redirect('parent_login')
        except:
            pass
        try:
            context['manager'] = Manager.objects.get(user = request.user)
            return redirect('manager_login')
        except:
            pass


    return render(request, 'index.html')

def team(request):
    context = {}

    return render('team.jinja', context)
