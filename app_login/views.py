from django.shortcuts import render, redirect
from logic.auth import check_user_before_registration, add_to_users_database, \
    check_user_before_authorization, authenticate, logout


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method == "POST":
        data = request.POST
        result = check_user_before_authorization(username=data["username"], password=data["password"])
        if result["answer"]:
            authenticate(username=data["username"])
            return redirect("/")
        return render(request, "login/login.html", context={"error": result["error"]})


def signup_view(request):
    if request.method == "GET":
        return render(request, "login/signup.html")

    if request.method == "POST":
        data = request.POST
        result = check_user_before_registration(username=data["username"], email=data["email"],
                                                password1=data["password1"], password2=data["password2"])
        if result["answer"]:
            add_to_users_database(username=data["username"], email=data["email"], password=data["password1"])
            # authenticate(data["username"])
            return redirect("/")
        return render(request, "login/signup.html", context={"error": result["error"]})


def logout_view(request):
    if request.method == "GET":
        logout()
        return redirect("/")
