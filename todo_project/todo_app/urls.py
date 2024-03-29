from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_tasks, name="my_tasks"),
]
