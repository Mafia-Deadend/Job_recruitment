from django.db import models



class JobApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    cv = models.FileField(upload_to='cvs/')  # Stores CV file path
    matched_skills = models.TextField(blank=True, null=True)
    match_percentage = models.FloatField(default=0)
    status = models.CharField(
        max_length=50,
        choices=[('Shortlisted', 'Shortlisted'), ('Waiting List', 'Waiting List'), ('Rejected', 'Rejected')],
        default="Pending"
    )

    def __str__(self):
        return f"{self.name} ({self.status})"


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()
    

    def __str__(self):
        return self.title