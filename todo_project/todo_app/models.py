from django.db import models


class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    task_name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name
