from django.contrib import messages
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render


def index(request):
    return render(request, "users/index.html")


def signup(request):
    error_messages = []

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        user = User.objects.filter(username=username).first()
        if isinstance(user, User):
            error_messages.append("User already exists")

        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            error_messages.extend(e.messages)

        if not error_messages:
            user = User.objects.create_user(username, email, password)
            user.save()
            messages.success(request, "Your account was created succesfully")
            return redirect("login")

    return render(request, "users/signup.html", {"error_messages": error_messages})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponse("Username or password incorrect")
    else:
        return render(request, "users/login.html")
