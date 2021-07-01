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
    if (action == 'post_add' or action == 'post_remove'):
        lvl = lesson.teacher.level

        num_students = len(lesson.students.all())
        duration = (lesson.end-lesson.start).total_seconds()/60

        students_deleted_pks = kwargs['pk_set']
        students_deleted = [Student.objects.get(pk = pk) for pk in students_deleted_pks]



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
        for student in students_deleted:
            sacc = StudentAccount.objects.get(student = student)

    if (action == 'pre_remove'):
        students_pk = kwargs['pk_set']
        students = [Student.objects.get(pk = pk) for pk in students_pk] # find all students to be removed
        for student in students:
            sacc = StudentAccount.objects.get(student = student)
            for bill in sacc.bills.all():
                if (bill.lesson == lesson):
                    bill.delete()
        



            


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



