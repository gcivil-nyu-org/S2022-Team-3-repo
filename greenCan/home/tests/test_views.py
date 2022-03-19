from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


class TestHomePage(TestCase):
    def setUp(self):
        self.url = reverse_lazy("home:index")

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "home/templates/index.html")
        self.assertEquals(response.status_code, 200)

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertContains(
            response, '<span class="slanted-btn-contain">Join Our Community!</span>'
        )
        self.assertNotContains(
            response,
            '<a class="dropdown-item" href="'
            + reverse("account:logout")
            + '">Logout</a>',
        )

    def test_authenticated_user(self):
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client._login(user)
        response = self.client.get(self.url)
        self.assertNotContains(
            response, '<span class="slanted-btn-contain">Join Our Community!</span>'
        )
        self.assertContains(
            response,
            '<a class="dropdown-item" href="'
            + reverse("account:logout")
            + '">Logout</a>',
        )
        self.assertContains(response, user.get_full_name().title())
