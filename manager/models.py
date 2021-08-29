from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from employee.models import Employee

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    employees = models.ManyToManyField(Employee)
    is_top = models.BooleanField(default = False)
    def __str__(self):
        return self.user.get_full_name()

class Request(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
