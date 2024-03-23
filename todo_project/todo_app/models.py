from django.db import models


class Task(models.Models):
    task_name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_done = models.BooleanField(default=False)
