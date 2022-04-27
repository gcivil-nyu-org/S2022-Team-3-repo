from django.urls import reverse
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class TestNotificationsViews(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email="testemail1@gmail.com",
            password="password1",
            first_name="john1",
            last_name="doe1",
        )

        self.user2 = User.objects.create(
            email="testemail2@gmail.com",
            password="password2",
            first_name="john2",
            last_name="doe2",
        )

        self.url = reverse("notification:index")

    def test_unauthenticated_users_GET(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("accounts:login") + f"?next={self.url}", 302)

    def test_authenticated_users_GET(self):
        self.client.force_login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertEquals(response, 200)
