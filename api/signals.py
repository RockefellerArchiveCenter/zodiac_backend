from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event, Package


@receiver(post_save, sender=Event)
def my_model_post_save(sender, instance, created, **kwargs):
    """Updates last_outcome field on parent package."""
    if created:
        package = Package.objects.get(pk=instance.package_identifier)
        package.last_outcome = package.event_set.all().order_by('-last_modified')[0].outcome
        package.save()
