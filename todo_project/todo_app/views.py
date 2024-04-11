from django.shortcuts import get_object_or_404, redirect, render
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
        task_id = request.POST.get("task_id")

        task = get_object_or_404(Task, pk=task_id)
        task.delete()
        return redirect("my_tasks")
    else:
        return render(request, "todo_app/mytasks.html")


def edit_task(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        title = request.POST.get("title")
        due_date = request.POST.get("due-date")
        description = request.POST.get("description")
        is_done = request.POST.get("done")
        print("\n\n\n\n valor do checkbox " + is_done + "\n\n\n\n\n")

        if due_date == "":
            due_date = None

        if description == "":
            description = None

        if is_done == "on":
            is_done = True
        else:
            is_done = False

        task = get_object_or_404(Task, pk=task_id)
        task.title = title
        task.due_date = due_date
        task.description = description
        task.is_done = is_done
        task.save()
        return redirect("my_tasks")
    else:
        return render(request, "todo_app/mytasks.html")
