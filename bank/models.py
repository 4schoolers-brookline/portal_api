from django.db import models
from activity.models import Lesson
from django.contrib.auth.models import User
from student.models import Student



class StudentAccount(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    units_left = models.FloatField(null = True, blank = True, default = 0)
    deposits = models.ManyToManyField('StudentDeposit')
    bills = models.ManyToManyField('StudentLessonBill')

class StudentDeposit(models.Model):
    units = models.FloatField(null=True, blank=True)
    dollars = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length = 250, null = True, blank = True)

class StudentLessonBill(models.Model):
    duration = models.IntegerField(null = True, blank = True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    coefficent = models.FloatField(null = True, blank = True, default = 1)
    
    def __str__(self):
        return ('{} (duration = {}, coeff = {})'.format(self.lesson.name, self.duration, self.coefficent))
