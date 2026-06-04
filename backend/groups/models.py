import uuid

from django.db import models
from user.models import User
from task.models import Task

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    members = models.ManyToManyField(User, related_name='member', blank=True)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    token = models.CharField(max_length = 100, unique = True, default=uuid.uuid4)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, related_name='invitations',
                                 null=False, blank=False)
    created_by = models.ForeignKey(User, related_name='invitations', null=False, blank=False, on_delete=models.CASCADE)
    expired_at = models.DateTimeField()