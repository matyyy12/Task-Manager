from django.db import models
from user.models import User
from task.models import Task

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    members = models.ManyToManyField(User, related_name='members', blank=True)

    def __str__(self):
        return self.name