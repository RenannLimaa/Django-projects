from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "users/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        user = User.objects.filter(username=username).first()
        if isinstance(user, User):
            return HttpResponse("User already exists")

        user = User.objects.create_user(username, email, password)
        user.save()
    else:
        return render(request, "users/signup.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse("Username or password incorrect")
    else:
        return render(request, "users/login.html")
