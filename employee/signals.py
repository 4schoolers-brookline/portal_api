import decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from manager.models import Manager
from django.db.models.signals import m2m_changed


@receiver(post_save, sender = Employee)
def employee_created(sender, instance, created, **kwargs):
    if (created):
        managers = Manager.objects.filter(is_top = True)
        for manager in managers:
            manager.employees.add(instance)
            manager.save()

    

    
