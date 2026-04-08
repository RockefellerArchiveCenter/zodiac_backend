from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Event


def set_status(instance):
    package = instance.package_identifier
    event_set = package.event_set.all().order_by('-last_modified')
    if event_set:
        last_event = event_set[0]
        if last_event.outcome == 'FAILURE':
            package.status = 'ERROR'
            package.error_message = last_event.message
        elif last_event.outcome == 'SUCCESS' and last_event.service == 'digital_ingest_transformation':
            package.status = 'COMPLETE'
            package.error_message = None
        else:
            package.status = 'IN PROCESS'
            package.error_message = None
    else:
        package.status = 'IN PROCESS'
        package.error_message = None
    package.save()


@receiver(post_save, sender=Event)
def update_status(sender, instance, created, **kwargs):
    """Updates status and error_message fields on parent package."""
    if created:
        set_status(instance)


@receiver(post_delete, sender=Event)
def clear_status(sender, instance, **kwargs):
    """Updates status and error_message fields on parent package."""
    set_status(instance)
