from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
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
        if user is not None:
            login_django(request, user)
            return redirect("logged_in")
        else:
            return HttpResponse("Username or password incorrect")
    else:
        return render(request, "users/login.html")


@login_required
def logged_in(request):
    username = request.user.username
    return render(request, "logged_in", {"username": username})


def logout(request):
    logout_django(request)
    return redirect("index")
