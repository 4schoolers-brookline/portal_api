from django.db import models
from django.contrib.auth.models import User
from student.models import Student


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    child = models.OneToOneField(Student, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()
