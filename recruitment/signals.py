from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobApplication, ShortlistedCandidate, WaitingListCandidate, RejectedCandidate

@receiver(post_save, sender=JobApplication)
def update_candidate_status(sender, instance, **kwargs):
    """
    When a JobApplication's status is changed, move the candidate to the correct table.
    """
    # Delete from all tables before adding to the correct one
    ShortlistedCandidate.objects.filter(job_application=instance).delete()
    WaitingListCandidate.objects.filter(job_application=instance).delete()
    RejectedCandidate.objects.filter(job_application=instance).delete()

    # Move to the correct table
    if instance.status == "Shortlisted":
        ShortlistedCandidate.objects.create(
            job_application=instance,
            job=instance.job,
            name=instance.name,
            cv=instance.cv
        )
    elif instance.status == "Waiting List":
        WaitingListCandidate.objects.create(
            job_application=instance,
            job=instance.job,
            name=instance.name,
            cv=instance.cv
        )
    elif instance.status == "Rejected":
        RejectedCandidate.objects.create(
            job_application=instance,
            job=instance.job,
            name=instance.name,
            cv=instance.cv
        )
