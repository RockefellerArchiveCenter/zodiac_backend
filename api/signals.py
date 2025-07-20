from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event


@receiver(post_save, sender=Event)
def update_status(sender, instance, created, **kwargs):
    """Updates status field on parent package."""
    if created:
        package = instance.package_identifier
        last_event = package.event_set.all().order_by('-last_modified')[0]
        if last_event.outcome == 'FAILURE':
            package.status = 'ERROR'
        elif last_event.outcome == 'SUCCESS' and last_event.service == 'digital_ingest_transformation':
            package.status = 'COMPLETE'
        else:
            package.status = 'IN PROCESS'
        package.save()
