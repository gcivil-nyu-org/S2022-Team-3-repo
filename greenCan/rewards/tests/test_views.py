from django.utils.encoding import force_str
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from reuse.tests.test_views import create_image
from django.core.files.uploadedfile import SimpleUploadedFile
from recycle.models import ZipCode
from rewards.models import Event, ImageMeta, Image, Category, CreditsLookUp

User = get_user_model()


class TestIndex(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testemail@gmail.com",
            password="password12",
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
        CreditsLookUp.objects.create(action="image", credit=5)
        self.url = reverse("rewards:earn-rewards")
        image = create_image(None, "test.png")
        image_file = SimpleUploadedFile("test.png", image.getvalue())
        image2 = create_image(None, "test2.png")
        image_file2 = SimpleUploadedFile("test2.png", image2.getvalue())
        event = Event(name="Recycle")
        category1 = Category(name="Plastic")
        category2 = Category(name="Other")
        category1.save()
        category2.save()
        event.save()

        self.data = {
            "file[]": [image_file, image_file2],
            "caption": "This is the caption!",
            "event": event.id,
            "location": "10001",
            "user": self.user.id,
            "consent": "consent",
        }

        self.data2 = self.data.copy()
        self.data2["categories[]"] = [category1.id, category2.id]

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

    def test_earn_rewards_valid_data_no_category_POST(self):
        """
        test to see if the request is stored into the database for value data
        """
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, self.data, follow=True)
        metas = ImageMeta.objects.all()
        self.assertEquals(len(metas), 1)
        images = Image.objects.all()
        self.assertEquals(len(images), 2)
        self.assertEquals(images[0].meta.approved, None)
        self.assertEquals(images[1].meta.approved, None)
        self.assertTrue(metas[0].consent)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, self.url, 302)
        self.assertEquals(message.tags, "success")
        self.assertEquals(
            message.message,
            "Request submitted successfully.",
        )

    def test_earn_rewards_valid_data_with_category_POST(self):
        """
        test to see if the request is stored into the database for value data
        """
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, self.data2, follow=True)
        metas = ImageMeta.objects.all()
        self.assertEquals(len(metas), 1)
        images = Image.objects.all()
        self.assertEquals(len(images), 2)
        self.assertEquals(len(metas[0].category.all()), 2)
        self.assertEquals(images[0].meta.approved, None)
        self.assertEquals(images[1].meta.approved, None)
        self.assertTrue(metas[0].consent)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, self.url, 302)
        self.assertEquals(message.tags, "success")
        self.assertEquals(
            message.message,
            "Request submitted successfully.",
        )

    def test_earn_rewards_valid_data_with_invalid_category_POST(self):
        """
        test to see if the request is stored into the database for value data
        """
        data = self.data2.copy()
        data["categories[]"] = [10]
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
            "Sorry, your request was not processed properly, please try again!",
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
        self.assertEquals(images[0].meta.approved, None)
        self.assertEquals(images[1].meta.approved, None)
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
        self.assertEquals(images[0].meta.approved, None)
        self.assertEquals(images[1].meta.approved, None)
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
        data["event"] = 4
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
            "You need to select an event, if none of the categories apply"
            ' in your case please select "Other".',
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
        event = Event(name="Recycle")
        event.save()
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

        user = User.objects.create_user(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
            is_active=True,
        )

        meta = ImageMeta(
            event_type=event,
            location=zipcode,
            caption="This is a caption",
            user=user,
            consent=True,
        )
        meta.save()

        image1 = Image(image="test1.png", meta=meta)
        image1.save()

        image2 = Image(image="test2.png", meta=meta)
        image2.save()

        meta2 = ImageMeta(
            event_type=event,
            location=zipcode,
            caption="<script>This is a caption</script>",
            user=user,
            consent=False,
        )
        meta2.save()
        image3 = Image(image="test3.png", meta=meta2)
        image3.save()

    def test_featured_image_gallery_GET(self):
        """
        test to verify the gallery page is accessible and using right template
        """
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "rewards/templates/featured-gallery.html")

    def test_featured_image_gallery_contains_csrf(self):
        """
        test to check that there is a csrf token in the view
        """
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_featured_image_gallery_valid_data_POST(self):
        """
        test to check that correct structure is return
        """
        data = {"page": 1}
        response = self.client.post(self.url, data, follow=True)
        self.assertJSONEqual(
            force_str(response.content),
            {
                "images": [
                    {
                        "image": "test2.png",
                        "event": "Recycle",
                        "description": "This is a caption",
                    },
                    {
                        "image": "test1.png",
                        "event": "Recycle",
                        "description": "This is a caption",
                    },
                ],
                "has_next": 0,
            },
        )

    def test_featured_image_gallery_no_page_number_POST(self):
        """
        test to check that page 1 is returned is post is an empty string.
        """
        data = {"page": ""}
        response = self.client.post(self.url, data, follow=True)
        self.assertJSONEqual(
            force_str(response.content),
            {
                "images": [
                    {
                        "image": "test2.png",
                        "event": "Recycle",
                        "description": "This is a caption",
                    },
                    {
                        "image": "test1.png",
                        "event": "Recycle",
                        "description": "This is a caption",
                    },
                ],
                "has_next": 0,
            },
        )
