from django.urls import path

from . import views

app_name = 'reuse'

urlpatterns = [
    # URLs here
    path('', views.listingPage, name='listingPage'),
]