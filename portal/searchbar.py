from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity
from django.core import serializers
import json

from parent.models import Parent
from manager.models import Manager
from employee.models import Employee
from student.models import Student
from django.db import connection
#with connection.cursor() as cursor:
#    cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')

def student_searchbar(request):
    query = Employee.objects.annotate(similarity=TrigramSimilarity('user__first_name', request.GET['value']),).filter(similarity__gt=0.55).order_by('-similarity')
    results = []
    for employee in query:
        results.append({"id": employee.id, "name": employee.user.get_full_name()})
    results = json.dumps(results)
    return JsonResponse(results, safe = False)

def employee_searchbar(request):
    query = Student.objects.annotate(similarity=TrigramSimilarity('user__first_name', request.GET['value']),).filter(similarity__gt=0.55).order_by('-similarity')
    results = []
    for student in query:
        results.append({"id": student.id, "name": student.user.get_full_name()})
    results = json.dumps(results)
    return JsonResponse(results, safe = False)
    pass

def manager_searchbar(request):
    query = Employee.objects.annotate(similarity=TrigramSimilarity('user__first_name', request.GET['value']),).filter(similarity__gt=0.55).order_by('-similarity')
    results = []
    for employee in query:
        results.append({"id": employee.id, "name": employee.user.get_full_name(), "type": "employee"})
    query = Student.objects.annotate(similarity=TrigramSimilarity('user__first_name', request.GET['value']),).filter(similarity__gt=0.55).order_by('-similarity')
    for student in query:
        results.append({"id": student.id, "name": student.user.get_full_name(), "type": "student"})
    results = json.dumps(results)
    return JsonResponse(results, safe = False)
    pass
