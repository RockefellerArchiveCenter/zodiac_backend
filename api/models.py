from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Package(models.Model):
    ORIGINS = [
        ('aurora', 'Aurora'),
        ('digitization', 'Digitization'),
        ('legacy_digital', 'Legacy Born Digital'),
        ('av_digitization', 'AV Digitization'),
    ]
    identifier = models.CharField(max_length=36, primary_key=True)
    origin = models.CharField(choices=ORIGINS, max_length=20)
    title = models.CharField(max_length=255)
    identifiers = models.JSONField(blank=True, null=True)
    rights_statements = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Event(models.Model):
    OUTCOMES = [
        ('STARTED', 'Started'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
    ]
    SERVICES = [
        ('ursa_major', 'Ursa Major'),
        ('fornax', 'Fornax'),
        ('webhook', 'Webhook'),
        ('aquarius', 'Aquarius')
    ]
    identifier = models.CharField(max_length=36, primary_key=True)
    outcome = models.CharField(choices=OUTCOMES)
    service = models.CharField(choices=SERVICES)
    package_identifier = models.ForeignKey(Package, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    traceback = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
