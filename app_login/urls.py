from django.urls import path
from .views import login_view, signup_view, logout_view

app_name = 'login'

urlpatterns = [
    path('', login_view, name="login_view"),
    path('signup/', signup_view, name="signup_view"),
    path('logout/', logout_view, name="logout_view"),
]