from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("create/", views.signup, name="create"),
    path("login/", views.login, name="login"),
    path("forget-password/", views.forget_password, name="forget-password"),
    path("reset-password/", views.reset_password, name="reset-password"),
]
