from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Package(models.Model):
    ORIGINS = [
        ('aurora', 'Aurora'),
        ('digitization', 'Digitization'),
        ('legacy_digital', 'Legacy Born Digital'),
        ('av_digitization', 'AV Digitization'),
    ]
    STATUSES = [
        ('IN PROCESS', 'In Process'),
        ('COMPLETE', 'Complete'),
        ('ERROR', 'Error'),
    ]
    identifier = models.CharField(max_length=36, primary_key=True)
    origin = models.CharField(choices=ORIGINS, max_length=20)
    title = models.CharField(max_length=255)
    identifiers = models.JSONField(blank=True, null=True)
    rights_statements = models.JSONField(blank=True, null=True)
    # created = models.DateTimeField(auto_now_add=True)
    # last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)
    status = models.CharField(choices=STATUSES, default='IN PROCESS')


class Event(models.Model):
    OUTCOMES = [
        ('STARTED', 'Started'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]
    SERVICES = [
        ('digital_ingest_discovery', 'Discovery'),
        ('digital_ingest_assembly', 'Assembly'),
        ('digital_ingest_webhook', 'Webhook'),
        ('digital_ingest_transformation', 'Transformation')
    ]
    identifier = models.CharField(max_length=36, primary_key=True)
    outcome = models.CharField(choices=OUTCOMES)
    service = models.CharField(choices=SERVICES)
    package_identifier = models.ForeignKey(Package, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    traceback = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
