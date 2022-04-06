from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from reuse.tests.test_views import create_image
from django.core.files.uploadedfile import SimpleUploadedFile
from recycle.models import ZipCode
from rewards.models import Event, ImageMeta, Image  # , Category

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
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + self.url, 302)


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
        image = create_image(None, "test.png")
        image_file = SimpleUploadedFile("test.png", image.getvalue())
        image2 = create_image(None, "test2.png")
        image_file2 = SimpleUploadedFile("test2.png", image2.getvalue())
        event = Event(name="Recycle")
        event.save()

        self.data = {
            "file[]": [image_file, image_file2],
            "caption": "This is the caption!",
            "event": event.id,
            "location": "10001",
            "user": self.user.id,
            "consent": "consent",
        }

        zipcode = ZipCode(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )

        zipcode.save()

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
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + self.url, 302)

    def test_earn_rewards_has_csrftoken(self):
        """
        test to check the csrf token is present in earn rewards page
        """
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_earn_rewards_valid_data_POST(self):
        """
        test to see if the request is stored into the database for value data
        """
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, self.data, follow=True)
        metas = ImageMeta.objects.all()
        self.assertEquals(len(metas), 1)
        images = Image.objects.all()
        self.assertEquals(len(images), 2)
        self.assertFalse(images[0].approved)
        self.assertFalse(images[1].approved)
        self.assertTrue(metas[0].consent)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, self.url, 302)
        self.assertEquals(message.tags, "success")
        self.assertEquals(
            message.message,
            "Request submitted successfully.",
        )

    def test_earn_rewards_valid_data_no_consent_POST(self):
        """
        test to see if the request is stored into the database for value data
        """
        data = self.data.copy()
        data["consent"] = ""
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data, follow=True)
        metas = ImageMeta.objects.all()
        self.assertEquals(len(metas), 1)
        images = Image.objects.all()
        self.assertEquals(len(images), 2)
        self.assertFalse(images[0].approved)
        self.assertFalse(images[1].approved)
        self.assertFalse(metas[0].consent)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, self.url, 302)
        self.assertEquals(message.tags, "success")
        self.assertEquals(
            message.message,
            "Request submitted successfully.",
        )

    def test_earn_rewards_valid_data_no_zipcode_POST(self):
        """
        test to see if the request with invalid data is not saved on database
        """
        data = self.data.copy()
        data["location"] = ""
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data, follow=True)
        metas = ImageMeta.objects.all()
        self.assertEquals(len(metas), 1)
        images = Image.objects.all()
        self.assertEquals(len(images), 2)
        self.assertFalse(images[0].approved)
        self.assertFalse(images[1].approved)
        self.assertTrue(metas[0].consent)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, self.url, 302)
        self.assertEquals(message.tags, "success")
        self.assertEquals(
            message.message,
            "Request submitted successfully.",
        )

    def test_earn_rewards_invalid_data_missing_image_POST(self):
        """
        test to see if the request with invalid data is not saved on database
        """
        data = self.data.copy()
        data["file[]"] = []
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data, follow=True)
        metas = ImageMeta.objects.all()
        self.assertEquals(len(metas), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, self.url, 302)
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "You need to upload at least one image to earn credits.",
        )

    def test_earn_rewards_invalid_data_event_POST(self):
        """
        test to see if the request with invalid data is not saved on database
        """
        data = self.data.copy()
        data["file[]"] = []
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data, follow=True)
        metas = ImageMeta.objects.all()
        self.assertEquals(len(metas), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, self.url, 302)
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "You need to upload at least one image to earn credits.",
        )

    def test_earn_rewards_invalid_data_zipcode_POST(self):
        """
        test to see if the request with invalid data is not saved on database
        """
        data = self.data.copy()
        data["location"] = "20030"
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data, follow=True)
        metas = ImageMeta.objects.all()
        self.assertEquals(len(metas), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, self.url, 302)
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Please enter a valid 5 digit NYC zipcode."
            " If it is not located in NYC please leave this field empty.",
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
