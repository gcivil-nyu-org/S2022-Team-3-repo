from django.test import SimpleTestCase
from django.urls import reverse, resolve

from account.views import signup_page, login_page, logout_view, activate_account_page


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
