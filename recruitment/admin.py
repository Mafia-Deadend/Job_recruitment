from django.contrib import admin
from .models import JobApplication  # Import your model

admin.site.register(JobApplication)  # Register the model
from .models import Job  # Import Job model if needed

admin.site.register(Job)
