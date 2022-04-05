from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from accounts.views import account_exists
from accounts.views import (
    signup_page,
    login_page,
    logout_view,
    activate_account_page,
    PasswordResetView,
    PasswordResetConfirmView,
    user_profile,
    user_profile_avatar,
)


class TestUrls(SimpleTestCase):
    def test_signup_url(self):
        url = reverse("accounts:create")
        resolved = resolve(url)
        self.assertEqual(resolved.func, signup_page)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/create/")

    def test_login_url(self):
        url = reverse("accounts:login")
        resolved = resolve(url)
        self.assertEqual(resolved.func, login_page)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/login/")

    def test_activate_url(self):
        url = reverse("accounts:activate", args=["uid", "token"])
        resolved = resolve(url)
        self.assertEqual(resolved.func, activate_account_page)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/activate/uid/token/")

    def test_logout_url(self):
        url = reverse("accounts:logout")
        resolved = resolve(url)
        self.assertEqual(resolved.func, logout_view)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/logout/")

    def test_password_reset_url(self):
        url = reverse("accounts:password-reset", args=["1", "7giugiugugiugiguigiugiug"])
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, PasswordResetConfirmView)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/reset/1/7giugiugugiugiguigiugiug/")

    def test_password_reset_sent_url(self):
        url = reverse("accounts:password-reset-sent")
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, PasswordResetDoneView)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/password-reset/sent/")

    def test_password_reset_done_url(self):
        url = reverse("accounts:password-reset-complete")
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, PasswordResetCompleteView)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/reset/done/")

    def test_forget_password_url(self):
        url = reverse("accounts:forget-password")
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, PasswordResetView)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/forgot-password/")

    # def test_social_url(self):
    #     url = reverse("socials:logout")
    #     resolved = resolve(url)
    #     self.assertEqual(resolved.func, signup_page)
    #     self.assertEqual(resolved.namespace, "accounts")
    #     self.assertEqual(url, "/accounts/create/")

    # testing profile urls
    def test_user_profile_url(self):
        url = reverse("accounts:user-profile")
        resolved = resolve(url)
        self.assertEqual(resolved.func, user_profile)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/user-profile/")

    def test_user_profile_avatar_url(self):
        url = reverse("accounts:user-profile-avatar")
        resolved = resolve(url)
        self.assertEqual(resolved.func, user_profile_avatar)
        self.assertEqual(resolved.namespace, "accounts")
        self.assertEqual(url, "/accounts/user-profile-avatar/")

    def test_social_profile_url(self):
        url = reverse("socialaccount_signup")
        resolved = resolve(url)
        self.assertEqual(resolved.func, account_exists)
        self.assertEqual(url, "/social/social/signup/")
