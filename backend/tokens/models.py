from django.db import models
from django.db import models
from django.utils import timezone
from datetime import timedelta
from user.models import User
import secrets

# Create your models here.


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='token')
    access_token = models.CharField(max_length=64, unique=True)
    refresh_token = models.CharField(max_length=64, unique=True)
    access_expires_at = models.DateTimeField(default=timezone.now)
    refresh_expires_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)


    @staticmethod
    def generate_key():
        return secrets.token_hex(32)

    @staticmethod
    def get_access_expiry():
        return timezone.now() + timedelta(minutes=15)

    @staticmethod
    def get_refresh_expiry():
        return timezone.now() + timedelta(days=7)

    def is_access_expired(self):
        return timezone.now() > self.access_expires_at

    def is_refresh_expired(self):
        return timezone.now() > self.refresh_expires_at