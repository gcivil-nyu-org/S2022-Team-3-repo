from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestModerationIndexPage(TestCase):
    def setUp(self):
        self.url = reverse("moderation:index")

    def test_unauthenticated_user(self):
        """
        test to verify only authenticated user can access
        the rewards index page unauthenticated user must
        be redirected to the login page
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + self.url, 302)

    def test_non_staff_cannot_access(self):
        """
        test non staff user cannot access this page
        """
        user = User.objects.create(
            email="testemail1@gmail.com",
            password="password2",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertRedirects(
            response, reverse("accounts:login") + "?next=" + self.url, 302, target_status_code=302
        )

    def test_only_volunteers_can_access(self):
        """
        test only staff/volunteers can access this page
        """
        volunteer = User.objects.create(
            email="testemail@gmail.com", password="password1", first_name="john", last_name="doe"
        )
        volunteer.staff = True
        volunteer.save()
        self.client.force_login(volunteer, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "moderation/templates/index.html")
