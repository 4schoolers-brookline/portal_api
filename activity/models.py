from django.db import models
from student.models import Student
from employee.models import Employee
from django.contrib.auth.models import User

SUBMISSION_TYPES = (
    ('Homework_Submission','Homework_Submission'),
    ('Classwork','Classwork'),
    ('Curriculum','Curriculum'),
    ('Homework', 'Homework')

)

SUBJECT_CHOICES = (
    ('Mathematics', 'Mathematics'),
    ('Computer Science', 'Computer Science'),
    ('English', 'English'),
    ('Chemistry', 'Chemistry'),
    ('Physics', 'Physics'),
    ('History', 'History'),
    ('Academic Advising','Academic Advising'),
    ('Compeetitive Math','Compeetitive Math'),
    ('Projects','Projects'),
    ('Essay Writing','Essay Writing'),
)


ACTIVITY_CHOICES = (
    ('Lesson','Lesson'),
    ('Advising','Advising'),
    ('Administrative','Administrative'),
    ('Other', 'Other')
)

ACC_TYPES = (
    ('student','student'),
    ('manager','manager'),
    ('employee','employee'),
    ('parent','parent')
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
    homework = models.OneToOneField('Submission', on_delete=models.CASCADE, related_name='lesson_homework_sent', null = True, blank = True)
    homework_submissions = models.ManyToManyField('Submission', null = True, blank = True)
    start = models.DateTimeField(null=True, blank = True)
    end = models.DateTimeField(null=True, blank = True)
    
    def __str__(self):
        return self.name


def user_submission(instance, filename):
    return ('{}s/id{}/{}/{}'.format(instance.account_type,instance.owner.id, instance.type, filename))

class Submission(models.Model):
    name = models.CharField(max_length=35,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length = 20, choices = ACC_TYPES, blank = True, null = True)
    type = models.CharField(max_length = 20, choices = SUBMISSION_TYPES)
    file = models.FileField(upload_to=user_submission, blank=True, null=True)
