from django.contrib import admin
from django.apps import AppConfig
from .models import JobApplication  # Import your model

admin.site.register(JobApplication)  # Register the model
from .models import Job  # Import Job model if needed

admin.site.register(Job)

class RecruitmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recruitment'

    def ready(self):
        import recruitment.signals 