from django.shortcuts import render, redirect
from logic.services import add_to_users, check_user, authenticate, logout

def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method == "POST":
        data = request.POST
        result = check_user(username=data["username"], password=data["password"])
        if result["answer"]:
            authenticate(data["username"])
            return redirect("store:shop_view")
        return render(request, "login/login.html", context={"error": result["error"]})

def signup_view(request):
    if request.method == "GET":
        return render(request, "login/signup.html")

    if request.method == "POST":
        data = request.POST
        result = add_to_users(username=data["username"], email=data["email"],
                              password1=data["password1"], password2=data["password2"])
        if result["answer"]:
            authenticate(data["username"])
            return redirect("store:shop_view")
        return render(request, "login/signup.html", context={"error": result["error"]})


def logout_view(request):
    if request.method == "GET":
        logout()
        return redirect("store:shop_view")

