from django.db import models
from django.contrib.auth.models import User
from student.models import Student


class Corporation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    children = models.ManyToManyField(Student)

    def __str__(self):
        return self.user.get_full_name()