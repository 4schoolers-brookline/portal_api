from django.contrib import admin
from .models import *

class StudentAccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentAccount, StudentAccountAdmin)

class StudentDepositAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentDeposit, StudentDepositAdmin)

class StudentLessonBillAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentLessonBill, StudentLessonBillAdmin)
