from django.db import models
from django.contrib.auth.models import User


def user_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return ('students/id{}/avatar.{}'.format(instance.user.id, ext))


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(null=True, blank=True)

    bio = models.CharField(max_length=215, null=True, blank=True)


    birth_date = models.DateField(null=True, blank=True)
    is_male = models.BooleanField(null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)

    image = models.ImageField(upload_to=user_image_path, null=True, blank = True, default = 'man.png')

    languages = models.CharField(max_length=215,null=True, blank=True)
    interests = models.CharField(max_length=215,null=True, blank=True)
    

    school = models.CharField(max_length=63,null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    
    address = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    zip_code = models.CharField(max_length=50,null=True, blank=True)
    state  = models.CharField(max_length=50,null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)

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

class Exam(models.Model):
    taker = models.ForeignKey('Student', on_delete = models.CASCADE)
    name = models.CharField(max_length = 215,null = True, blank = True)
    score = models.FloatField(null = True, blank = True)
    percentage = models.IntegerField(null = True, blank = True)




