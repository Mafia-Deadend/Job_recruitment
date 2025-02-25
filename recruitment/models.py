from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255, unique=True)  # Unique job titles
    description = models.TextField()
    required_skills = models.TextField()

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)  # Dropdown in forms
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    )
    cv = models.FileField(upload_to='cvs/')
    matched_skills = models.TextField(blank=True, null=True)
    match_percentage = models.FloatField(default=0)
    status = models.CharField(
        max_length=50,
        choices=[('Shortlisted', 'Shortlisted'), ('Waiting List', 'Waiting List'), ('Rejected', 'Rejected')],
        default="Pending"
    )

    def __str__(self):
        return f"{self.name} ({self.job.title if self.job else 'No Job'} - {self.status})"


class ShortlistedCandidate(models.Model):
    job_application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cvs/')

    def __str__(self):
        return f"{self.name} - Shortlisted"


class WaitingListCandidate(models.Model):
    job_application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cvs/')

    def __str__(self):
        return f"{self.name} - Waiting List"


class RejectedCandidate(models.Model):
    job_application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cvs/')

    def __str__(self):
        return f"{self.name} - Rejected"
