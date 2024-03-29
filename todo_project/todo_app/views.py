from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
# Create your views here.


def my_tasks(request):
    tasks = Task.objects.all()
    return render(request, "todo_app/mytasks.html", {"tasks": tasks})
