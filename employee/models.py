from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_fulltime = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    
    birth_date = models.DateField(null=True, blank=True)
    is_male = models.BooleanField(null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)

    bio = models.TextField(blank=True, null=True)
    school = models.CharField(max_length=63,null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    
    address = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    zip_code = models.CharField(max_length=50,null=True, blank=True)
    state  = models.CharField(max_length=50,null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)
    
    level = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return self.user.get_full_name()

class Documents(models.Model):
    name = models.CharField(max_length=35,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to ='uploads/')