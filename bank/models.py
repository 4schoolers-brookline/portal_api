from django.db import models
from activity.models import Lesson
from django.contrib.auth.models import User
from student.models import Student



class StudentAccount(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    deposits = models.ManyToManyField('StudentDeposit', null = True, blank = True,)
    bills = models.ManyToManyField('StudentLessonBill', null = True, blank = True,)
    def __str__(self):
        return (self.student.user.first_name)

    def get_units_left(self):
        s = 0
        for bill in self.bills.all():
            s -= round((bill.duration * bill.coefficent)/60,2)
        for deposit in self.deposits.all():
            s += round(deposit.units)
        return round(s,2)

class StudentDeposit(models.Model):
    units = models.FloatField(null=True, blank=True)
    dollars = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length = 250, null = True, blank = True)

    def __str__(self):
        return ('{} units: {}'.format(self.units, self.description))

class StudentLessonBill(models.Model):
    duration = models.IntegerField(null = True, blank = True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    coefficent = models.FloatField(null = True, blank = True, default = 1)

    def __str__(self):
        return ('{} (duration = {}, coeff = {})'.format(self.lesson.name, self.duration, self.coefficent))
