from django.apps import AppConfig


class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'student'
    def ready(self):
        import student.signals
