from django.urls import path

from . import views

app_name = "reuse"

urlpatterns = [
    path("", views.index, name="index"),
    path("donations/", views.donation_view, name="donation-page"),
    path("listings/", views.listing_page, name="listing-page"),
    path("create_post/", views.create_post, name="create-post"),
    path("ngo_donation/", views.ngo_donation, name="ngo-donation"),
    path(
        "fetch-ngo-locations/",
        views.search_ngo_locations,
        name="fetch-ngo-locations",
    ),
    path("my-posts/", views.my_posts, name="my-posts"),
    path("post-availability/", views.post_availability, name="post-availability"),
    path("post-details/", views.post_details, name="post-details"),
    path("raise-concerns/", views.raise_concerns, name="raise-concerns"),
]
