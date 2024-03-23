from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logged_in", views.logged_in, name="logged_in"),
    path("logout/", views.logout, name="logout"),
]
