from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.BigIntegerField()
    location = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'

class Group(models.Model):
    group_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members')

    class Meta:
        db_table = 'group'


class Messages(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'message'
