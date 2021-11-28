from django.urls import path

from users.views import UserCreateView, UserTiresInfoView, login

app_name = "users"

urlpatterns = [
    path("", UserCreateView.as_view()),
    path("login/", login),
    path("<str:username>/", UserTiresInfoView.as_view()),
]
