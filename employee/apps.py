from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'employee'
    def ready(self):
        import employee.signals