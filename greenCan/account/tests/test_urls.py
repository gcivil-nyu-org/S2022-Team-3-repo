from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView
from account.views import (
    signup_page,
    login_page,
    logout_view,
    activate_account_page,
    PasswordResetView,
    PasswordResetConfirmView,
)


class TestUrls(SimpleTestCase):
    def test_signup_url(self):
        url = reverse("account:create")
        resolved = resolve(url)
        self.assertEqual(resolved.func, signup_page)
        self.assertEqual(resolved.namespace, "account")
        self.assertEqual(url, "/account/create/")

    def test_login_url(self):
        url = reverse("account:login")
        resolved = resolve(url)
        self.assertEqual(resolved.func, login_page)
        self.assertEqual(resolved.namespace, "account")
        self.assertEqual(url, "/account/login/")

    def test_activate_url(self):
        url = reverse("account:activate", args=["uid", "token"])
        resolved = resolve(url)
        self.assertEqual(resolved.func, activate_account_page)
        self.assertEqual(resolved.namespace, "account")
        self.assertEqual(url, "/account/activate/uid/token/")

    def test_logout_url(self):
        url = reverse("account:logout")
        resolved = resolve(url)
        self.assertEqual(resolved.func, logout_view)
        self.assertEqual(resolved.namespace, "account")
        self.assertEqual(url, "/account/logout/")

    def test_password_reset_url(self):
        url = reverse("account:password-reset", args=["1", "7giugiugugiugiguigiugiug"])
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, PasswordResetConfirmView)
        self.assertEqual(resolved.namespace, "account")
        self.assertEqual(url, "/account/reset/1/7giugiugugiugiguigiugiug/")

    def test_password_reset_sent_url(self):
        url = reverse("account:password-reset-sent")
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, PasswordResetDoneView)
        self.assertEqual(resolved.namespace, "account")
        self.assertEqual(url, "/account/password-reset/sent/")

    def test_password_reset_done_url(self):
        url = reverse("account:password-reset-complete")
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, PasswordResetCompleteView)
        self.assertEqual(resolved.namespace, "account")
        self.assertEqual(url, "/account/reset/done/")

    def test_forget_password_url(self):
        url = reverse("account:forget-password")
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, PasswordResetView)
        self.assertEqual(resolved.namespace, "account")
        self.assertEqual(url, "/account/forgot-password/")
