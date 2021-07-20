from django.contrib import admin
from .models import Manager, Request

class ManagerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Manager, ManagerAdmin)

class RequestAdmin(admin.ModelAdmin):
    pass
admin.site.register(Request, RequestAdmin)
