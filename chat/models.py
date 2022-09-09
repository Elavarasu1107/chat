from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.BigIntegerField()
    location = models.CharField(max_length=150)


class Messages(models.Model):
    room_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
