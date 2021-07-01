from django.contrib import admin
from .models import *
from django import forms

class StudentAccountAdmin(admin.ModelAdmin):
    readonly_fields = ('units_left',)

    def units_left(self, obj):
        return (obj.get_units_left())

admin.site.register(StudentAccount, StudentAccountAdmin)

class StudentDepositAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentDeposit, StudentDepositAdmin)

class StudentLessonBillAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentLessonBill, StudentLessonBillAdmin)
