from django.db import models
from user.models import User
from category.models import Category

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_to = models.DateField()
    completed = models.BooleanField(default=False)

    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category',
                                 null=True, blank=True)

    def __str__(self):
        return (f"title: {self.title}\n"
                f"description: {self.description}\n"
                f", due_to: {self.due_to}\n"
                f", completed: {self.completed}\n"
                f"assigned_to: {self.assigned_to}\n"
                f"category: {self.category}\n")