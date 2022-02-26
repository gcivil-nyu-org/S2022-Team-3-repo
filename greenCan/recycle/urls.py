from django.urls import path

from . import views

app_name = 'recycle'

urlpatterns = [
    path('', views.index, name='index')
]