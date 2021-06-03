from django.contrib import admin
from .models import Parent

class ParentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Parent, ParentAdmin)
