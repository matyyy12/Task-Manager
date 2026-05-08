from django.db import models
from user.models import User

class Task(models.Model):
    class Category(models.TextChoices):
        TODO = 'TODO', 'To do'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        DONE = 'DONE', 'Done'


    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    due_to = models.DateField()
    completed = models.BooleanField(default=False)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.TODO,
    )

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_to', null=True, blank=True)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return (f"title: {self.title}\n"
                f"description: {self.description}\n"
                f", due_to: {self.due_to}\n"
                f", completed: {self.completed}\n"
                f"assigned_to: {self.assigned_to}\n"
                f"category: {self.category}\n")