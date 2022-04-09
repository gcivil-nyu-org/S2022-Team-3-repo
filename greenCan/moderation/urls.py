from django.urls import path

from . import views

app_name = "moderation"

urlpatterns = [
    path("", views.index, name="index"),
]
