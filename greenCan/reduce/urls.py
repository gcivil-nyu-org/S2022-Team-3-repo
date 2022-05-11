from django.urls import path

from . import views

app_name = "reduce"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "fetch-retailer-locations/",
        views.search_retailer_locations,
        name="fetch-retailer-locations",
    ),
]
