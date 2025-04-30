from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event


@receiver(post_save, sender=Event)
def update_last_outcome(sender, instance, created, **kwargs):
    """Updates last_outcome field on parent package."""
    if created:
        package = instance.package_identifier
        package.last_outcome = package.event_set.all().order_by('-last_modified')[0].outcome
        package.save()
