from django.urls import path

from . import views


app_name = "helper"

urlpatterns = [
    path("400/", views.error400, name="400"),
    path("404/", views.error404, name="404"),
    path("500/", views.error500, name="500"),
    path("505/", views.error505, name="505")
]
