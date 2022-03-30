from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from PIL import Image as Img
from six import BytesIO
from recycle.models import ZipCode
from reuse.models import Image, Post

User = get_user_model()


def create_image(
    storage, filename, size=(100, 100), image_mode="RGB", image_format="PNG"
):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Img.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class TestCreatePost(TestCase):
    def setUp(self):
        self.url = reverse("reuse:create-post")
        self.redirect_url = reverse("reuse:donation-page")
        self.login_redirect_url = reverse("accounts:login") + "?next=" + self.url
        image = create_image(None, "test.png")
        image_file = SimpleUploadedFile("test.png", image.getvalue())
        image2 = create_image(None, "test2.png")
        image_file2 = SimpleUploadedFile("test2.png", image2.getvalue())
        self.data = {
            "file[]": [image_file, image_file2],
            "title": "Bed",
            "description": "Twin bed",
            "zipcode": "10001",
            "number": "9999999998",
            "email": "kevin@gmail.com",
            "category": "Furniture",
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

    def test_unauthenticated(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        self.assertRedirects(response, self.login_redirect_url, 302)
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)

    def test_auth_valid_form(self):
        data = self.data.copy()
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 1)
        images = Image.objects.all()
        self.assertEquals(len(images), 2)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_1(self):
        data = self.data.copy()
        del data["title"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_2(self):
        data = self.data.copy()
        del data["description"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_3(self):
        data = self.data.copy()
        del data["zipcode"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_4(self):
        data = self.data.copy()
        del data["category"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_5(self):
        data = self.data.copy()
        data["zipcode"] = "10002"
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        self.assertRedirects(response, self.redirect_url, 302)


class TestViews(TestCase):
    def setUp(self):
        self.index_url = reverse("reuse:index")
        self.donation_page_url = reverse("reuse:donation-page")
        self.listingPage_url = reverse("reuse:listingPage")
        self.create_post_url = reverse("reuse:create-post")
        self.client = Client()

    def test_index_GET(self):

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse_index.html")

    def test_donationpage_GET(self):

        response = self.client.get(self.donation_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse/templates/donate-item-page.html")

    def test_listingPage_GET(self):

        response = self.client.get(self.listingPage_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "listing-page.html")
