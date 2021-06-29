import decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from student.models import Student

@receiver(post_save, sender = Student)
def create_initial_account(sender, instance, created, **kwargs):
    if (created):
        StudentAccount.objects.create(student = instance, units_left = 0)


# @receiver(post_save, sender = Student)
# def create_initial_account(sender, instance, created, **kwargs):
#     if (created):
#         StudentAccount.objects.create(student = instance, units_left = 0)


