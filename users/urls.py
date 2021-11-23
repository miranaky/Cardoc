from django.urls import path

from users.views import UserCreateView, login

app_name = "users"

urlpatterns = [
    path("", UserCreateView.as_view()),
    path("login/", login),
]
