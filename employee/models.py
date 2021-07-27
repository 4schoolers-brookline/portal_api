from django.db import models
from django.contrib.auth.models import User

def user_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return ('employees/id{}/avatar.{}'.format(instance.user.id, ext))


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_fulltime = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True)
    title = models.CharField(max_length=100,null=True, blank=True)

    education = models.CharField(max_length=180,null=True, blank=True)
    priority = models.IntegerField(default = 10, null=True, blank=True)
    image = models.ImageField(upload_to=user_image_path, null=True, blank = True, default = 'man.png')


    languages = models.CharField(max_length=215,null=True, blank=True)
    interests = models.CharField(max_length=215,null=True, blank=True)
    subjects = models.CharField(max_length=255,null=True, blank=True)


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

    def get_languages(self):
        langs = self.languages
        try:
            x = langs.split(',')
            return x
        except:
            return []
        
    def get_interests(self):
        ints = self.interests
        try:
            x = ints.split(',')
            return x
        except:
            return []
    def get_subjects(self):
        subs = self.subjects
        try:
            x = subs.split(',')
            return x
        except:
            return []

class Documents(models.Model):
    name = models.CharField(max_length=35,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to ='uploads/')
