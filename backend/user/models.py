from django.db import models


class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    def __str__(self):
        return self.username