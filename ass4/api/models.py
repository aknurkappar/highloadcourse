from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Email(models.Model):
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    secret_info = models.CharField(max_length=6, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)

class AudioUpload(models.Model):
    file = models.FileField(upload_to='audio_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, default='pending')
    progress = models.PositiveIntegerField(default=0)
