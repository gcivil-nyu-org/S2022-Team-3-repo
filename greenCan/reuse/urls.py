from django.urls import path

from . import views

app_name = "reuse"

urlpatterns = [
    path("donations", views.donation_view, name="donation-page"),
]
