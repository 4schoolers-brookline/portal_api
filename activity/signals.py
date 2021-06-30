import decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from student.models import Student
from bank.models import *
from django.db.models.signals import m2m_changed


@receiver(m2m_changed, sender = Lesson.students.through)
def students_lesson_changed(sender, **kwargs):
    lesson = kwargs['instance']
    action = kwargs['action']
    if (action == 'post_add'):
        lvl = lesson.teacher.level

        num_students = len(lesson.students.all())
        duration = (lesson.end-lesson.start).total_seconds()/60

        if (num_students == 1):
            coeff = 1
        elif (num_students == 2):
            coeff = 0.7
        elif (num_students > 2 ):
            coeff = 0.5
        
        if (lvl == 1):
            coeff *= 0.5
        elif (lvl == 2):
            coeff *= 0.7
        elif (lvl > 2):
            coeff *= 1

        for student in lesson.students.all():
            student_acc = StudentAccount.objects.get(student = student)
            try:
                bill = student_acc.bills.get(lesson = lesson)
                bill.coefficent = coeff
                bill.duration = duration
                bill.save()
            except:
                bill = StudentLessonBill(lesson = lesson, coefficent = coeff, duration = duration)
                bill.save()
                student_acc.bills.add(bill)

            
            


@receiver(post_save, sender = Lesson)
def lesson_changed(sender, instance, created, **kwargs):
  
    lesson = instance
    lvl = lesson.teacher.level

    num_students = len(lesson.students.all())
    duration = (lesson.end-lesson.start).total_seconds()/60

    coeff = 1

    if (num_students == 1):
        coeff = 1
    elif (num_students == 2):
        coeff = 0.7
    elif (num_students > 2 ):
        coeff = 0.5
    

    if (lvl == 1):
        coeff *= 0.5
    elif (lvl == 2):
        coeff *= 0.7
    elif (lvl > 2):
        coeff *= 1

    
    for student in lesson.students.all():
        if (not created):
            student_acc = StudentAccount.objects.get(student = student)
            bill = student_acc.bills.get(lesson = lesson)
            bill.coefficent = coeff
            bill.duration = duration
            bill.save()

        else:
            student_acc = StudentAccount.objects.get(student = student)
            bill = StudentLessonBill(lesson = lesson, coefficient = coeff, duration = duration)
            bill.save()
            student_acc.bills.add(bill)
            student_acc.save()



