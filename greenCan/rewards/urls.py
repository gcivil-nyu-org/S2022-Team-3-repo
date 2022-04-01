from django.urls import path

from . import views

app_name = "rewards"

urlpatterns = [
    path("", views.index, name="index"),
    path("earn/", views.earn_rewards, name="earn-rewards"),
]
