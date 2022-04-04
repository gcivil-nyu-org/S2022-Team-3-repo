from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class TestIndex(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
            is_active=True,
        )
        self.url = reverse("rewards:index")

    def test_index_authenticated_GET(self):
        """
        test to verify only authenticated user
        can access the rewards index page
        """
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "rewards/templates/index.html")

    def test_index_not_authenticated_GET(self):
        """
        test to verify only authenticated user can access
        the rewards index page unauthenticated user must
        be redirected to the login page
        """
        response = self.client.get(self.url)
        self.assertRedirects(
            response, reverse("accounts:login") + "?next=" + self.url, 302
        )


class TestEarnRewards(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
            is_active=True,
        )
        self.url = reverse("rewards:earn-rewards")

    def test_earn_rewards_authenticated_GET(self):
        """
        test to verify only authenticated user
        can access the rewards earn page
        """
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "rewards/templates/earn-rewards.html")

    def test_earn_rewards_not_authenticated_GET(self):
        """
        test to verify only authenticated user can access the rewards earn page
        unauthenticated user must be redirected to the login page
        """
        response = self.client.get(self.url)
        self.assertRedirects(
            response, reverse("accounts:login") + "?next=" + self.url, 302
        )


class TestFeaturedGallery(TestCase):
    def setUp(self):
        self.url = reverse("rewards:featured-image-gallery")

    def test_featured_image_gallery_GET(self):
        """
        test to verify the gallery page is accessible and using right template
        """
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "rewards/templates/featured-gallery.html")
