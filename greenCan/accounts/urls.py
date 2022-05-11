from django.urls import path
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from .views import (
    PasswordResetView,
    PasswordResetConfirmView,
    green_credits_logs,
    volunteer_registration,
)

from .views import (
    signup_page,
    login_page,
    logout_view,
    activate_account_page,
    user_profile,
    user_profile_avatar,
    get_questions,
)

app_name = "accounts"

urlpatterns = [
    path("create/", signup_page, name="create"),
    path(
        "activate/<slug:uidb64>/<slug:token>/",
        activate_account_page,
        name="activate",
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
        PasswordResetConfirmView.as_view(template_name="accounts/templates/reset-password.html"),
        name="password-reset",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/templates/reset-password-done.html"
        ),
        name="password-reset-complete",
    ),
    path("user-profile/", user_profile, name="user-profile"),
    path("user-profile-avatar/", user_profile_avatar, name="user-profile-avatar"),
    path("green-credits-logs/", green_credits_logs, name="green-credits-logs"),
    path("volunteer/registration/", volunteer_registration, name="volunteer-registration"),
    path("application-questions/", get_questions, name="fetch-questions"),
]
