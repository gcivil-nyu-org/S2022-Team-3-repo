from django.urls import path
from django.contrib.auth import views as auth_views

from .views import signup_page, login_page, logout_view, activate_account_page

app_name = "account"

urlpatterns = [
    path("create/", signup_page, name="create"),
    path(
        "activate/<slug:uidb64>/<slug:token>/", activate_account_page, name="activate"
    ),
    path("login/", login_page, name="login"),
    path("logout/", logout_view, name="logout"),
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="account/templates/forget-password.html"
        ),
        name="forget-password",
    ),
    path(
        "password_reset/sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/templates/forget-password-done.html"
        ),
        name="password-reset-sent",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/templates/reset-password.html"
        ),
        name="password-reset",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/templates/reset-password-done.html"
        ),
        name="password-reset-complete",
    ),
]
