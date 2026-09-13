from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def Register_View(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password confirmation
        if password != confirm_password:
            return HttpResponse("Password does not match")

        # Username already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("User already registered")

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "register.html")


def Login_View(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        return HttpResponse("Invalid username or password")

    return render(request, "login.html")


def Logout_View(request):

    logout(request)

    return redirect("login")