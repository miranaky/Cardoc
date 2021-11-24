from django.urls import path

from tires.views import CreateTiresInfoView

app_name = "tires"

urlpatterns = [
    path("", CreateTiresInfoView.as_view()),
]
