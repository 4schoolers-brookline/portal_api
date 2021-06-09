from django.db import models
from student.models import Student
from employee.models import Employee
from django.contrib.auth.models import User

SUBMISSION_TYPES = (
    ('homework','homework'),
    ('classwork','classwork'),
    ('curriculum','curriculum'),
    ('',''),
    ('',''),
    ('',''),
    ('',''),
)

SUBJECT_CHOICES = (
    ('Calculus', 'Calculus'),
    ('Computer Science', 'Computer Science'),
    ('English', 'English'),
    ('Chemistry', 'Chemistry'),
    ('Physics', 'Physics'),
    ('History', 'History'),
    ('Academic Advising','Academic Advising'),
    ('Advanced Math','Advanced Math')
)

SUBJECT_CHOICES = (
    ('Calculus', 'Calculus'),
    ('Computer Science', 'Computer Science'),
    ('English', 'English'),
    ('Chemistry', 'Chemistry'),
    ('Physics', 'Physics'),
    ('History', 'History'),
    ('Academic Advising','Academic Advising'),
    ('Advanced Math','Advanced Math')
)

ACTIVITY_CHOICES = (
    ('Lesson','Lesson'),
    ('Advising','Advising'),
    ('Administrative','Administrative'),
    ('Other', 'Other')
)

class Activity(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    type = models.CharField(max_length = 30, choices = ACTIVITY_CHOICES)
    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(max_length=50,null=True, blank=True)
    description = models.TextField(blank=True, null=True)



class Lesson(models.Model):
    students = models.ManyToManyField(Student)
    teacher = models.OneToOneField(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length = 30, choices = SUBJECT_CHOICES, default = '1')
    classwork = models.OneToOneField('Submission', on_delete=models.CASCADE, related_name='lesson_classwork', null = True, blank = True)
    homework_sent = models.OneToOneField('Submission', on_delete=models.CASCADE, related_name='lesson_homework_sent', null = True, blank = True)
    homework_submissions = models.ManyToManyField('Submission', null = True, blank = True)
    start = models.DateTimeField(null=True, blank = True)
    end = models.DateTimeField(null=True, blank = True)
    
    def __str__(self):
        return self.name


class Submission(models.Model):
    name = models.CharField(max_length=35,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length = 20, choices = SUBMISSION_TYPES)
    file = models.FileField(upload_to ='uploads/', blank=True, null=True)
