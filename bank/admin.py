from django.contrib import admin
from .models import *

class StudentAccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentAccount, StudentAccountAdmin)
