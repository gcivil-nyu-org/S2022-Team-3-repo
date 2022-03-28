from django.urls import path

from . import views

app_name = "recycle"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "fetch-drop-off-locations",
        views.search_dropoff_locations,
        name="fetch-drop-off-locations",
    )
]
