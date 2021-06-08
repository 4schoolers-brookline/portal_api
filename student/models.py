from django.db import models
from django.contrib.auth.models import User
import os
from django.dispatch import receiver

def user_folder(instance, filename):
    return ('media/students/id{}/{}'.format(instance.user.id, filename))


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)
    is_male = models.BooleanField(null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    
    image = models.ImageField(upload_to=user_folder, null=True, blank = True)

    school = models.CharField(max_length=63,null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    
    address = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    zip_code = models.CharField(max_length=50,null=True, blank=True)
    state  = models.CharField(max_length=50,null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)
    
    wallet = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()
