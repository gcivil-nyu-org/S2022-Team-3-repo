from django.urls import path

from . import views

app_name = "reuse"

urlpatterns = [
    path("", views.index, name="reuse-landing-page"),
    path("donations", views.donation_view, name="donation-page"),
    path('listings', views.listingPage, name='listingPage'),
    path('create_post', views.create_post, name='create-post')
]



