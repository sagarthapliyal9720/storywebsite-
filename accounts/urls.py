from django.urls import path
from .views import Register_View, Login_View, Logout_View


urlpatterns = [
    path("register/", Register_View, name="register"),
    path("login/", Login_View, name="login"),
    path("logout/", Logout_View, name="logout"),
]