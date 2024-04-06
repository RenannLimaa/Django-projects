from django.shortcuts import render, redirect
from .models import Task
# Create your views here.


def my_tasks(request):
    tasks = Task.objects.all()
    return render(request, "todo_app/mytasks.html", {"tasks": tasks})


def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due-date")
        description = request.POST.get("description")

        if due_date == "":
            due_date = None

        elif description == "":
            description = None

        task = Task(task_name=title, description=description, due_date=due_date)
        task.save()

        return redirect("my_tasks")
    else:
        return render(request, "todo_app/mytasks.html")


def delete_task(request):
    if request.method == "POST":
        title = request.POST.get("title")

        task = Task.objects.get(task_name=title)
        task.delete()
        return redirect("my_tasks")
    else:
        return render(request, "todo_app/mytasks.html")


def edit_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        due_date = request.POST.get("due-date")
        description = request.POST.get("description")

        if due_date == "":
            due_date = None

        elif description == "":
            description = None

        task = Task(task_name=title, description=description, due_date=due_date)
    else:
        return render(request, "todo_app/mytasks.html")
