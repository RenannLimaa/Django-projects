from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_tasks, name="my_tasks"),
    path("add/", views.add_task, name="add_task"),
    path("delete/", views.delete_task, name="delete_task"),
]
