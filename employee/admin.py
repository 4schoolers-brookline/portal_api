from django.contrib import admin

from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Employee, EmployeeAdmin)

admin.site.site_header = '4Schoolers Portal IT Panel'
admin.site.site_title = '4Schoolers IT Admin Panel'