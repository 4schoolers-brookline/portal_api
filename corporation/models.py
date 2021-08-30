from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from employee.models import Employee

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    children = models.ManyToManyField(Employee)

    def __str__(self):
        return self.user.get_full_name()