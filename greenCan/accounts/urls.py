from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from .views import PasswordResetView, PasswordResetConfirmView

from .views import signup_page, login_page, logout_view, activate_account_page

app_name = "accounts"

urlpatterns = [
    path("create/", signup_page, name="create"),
    path(
        "activate/<slug:uidb64>/<slug:token>/", activate_account_page, name="activate"
    ),
    path("login/", login_page, name="login"),
    path("logout/", logout_view, name="logout"),
    path(
        "forgot-password/",
        PasswordResetView.as_view(
            template_name="accounts/templates/forget-password.html",
            html_email_template_name="email/email-forgot-password.html",
        ),
        name="forget-password",
    ),
    path(
        "password-reset/sent/",
        PasswordResetDoneView.as_view(
            template_name="accounts/templates/forget-password-done.html"
        ),
        name="password-reset-sent",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/templates/reset-password.html"
        ),
        name="password-reset",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/templates/reset-password-done.html"
        ),
        name="password-reset-complete",
    ),
]
