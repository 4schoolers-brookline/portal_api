from django.contrib import admin
from .models import Lesson, Submission, Activity


class ActivityAdmin(admin.ModelAdmin):
    pass
class LessonAdmin(admin.ModelAdmin):
    pass
class SubmissionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Lesson, LessonAdmin)