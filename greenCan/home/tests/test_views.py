from django.conf import settings
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from rewards.models import EarnGreenCredits, CreditsLookUp, Event, ImageMeta, Image, Category
from recycle.models import ZipCode
from reuse.models import Post
from reuse.tests.test_views import create_image
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class TestHomePage(TestCase):
    def setUp(self):
        self.url = reverse_lazy("home:index")
        user1 = User.objects.create(
            email="testemail1@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )

        user2 = User.objects.create(
            email="testemail2@gmail.com",
            password="password2",
            first_name="john2",
            last_name="doe2",
        )

        user3 = User.objects.create(
            email="testemail3@gmail.com",
            password="password3",
            first_name="john3",
            last_name="doe3",
        )

        CreditsLookUp.objects.create(action="post", credit=10)
        CreditsLookUp.objects.create(action="image", credit=5)

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
        post1 = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=user1,
        )
        post1.save()
        #self.zipcode = zipcode

        EarnGreenCredits.objects.create(
                object_id=post1.id,
                content_object=post1,
                action=CreditsLookUp.objects.get(action="post"),
                user=user1,
        )

        post2 = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=user2,
        )
        post2.save()

        EarnGreenCredits.objects.create(
                object_id=post2.id,
                content_object=post2,
                action=CreditsLookUp.objects.get(action="post"),
                user=user2,
        )

        post3 = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=user3,
        )
        post3.save()

        EarnGreenCredits.objects.create(
                object_id=post3.id,
                content_object=post3,
                action=CreditsLookUp.objects.get(action="post"),
                user=user3,
        )
    

        event = Event(name="Recycle")
        event.save()

        meta1 = ImageMeta(
            caption = "This is the caption!",
            event_type = event,
            location = zipcode,
            user =  user1,
            consent = True,
        )
        meta1.save()

        meta2 = ImageMeta(
            caption = "This is the caption!",
            event_type =  event,
            location = zipcode,
            user = user2,
            consent = True,
        )
        meta2.save()

        EarnGreenCredits.objects.create(
                object_id=meta1.id,
                content_object=meta1,
                action=CreditsLookUp.objects.get(action="image"),
                user=user1,
        )

        EarnGreenCredits.objects.create(
                object_id=meta2.id,
                content_object=meta2,
                action=CreditsLookUp.objects.get(action="image"),
                user=user2,
        )



    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "home/templates/index.html")
        self.assertEquals(response.status_code, 200)

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertContains(
            response,
            '<span class="slanted-btn-contain">Join Our Community!</span>',
        )
        self.assertNotContains(
            response,
            '<a class="dropdown-item" href="' + reverse("accounts:logout") + '">Logout</a>',
        )

    def test_authenticated_user(self):
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )

        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertNotContains(
            response,
            '<span class="slanted-btn-contain">Join Our Community!</span>',
        )
        self.assertContains(
            response,
            '<a class="dropdown-item" href="' + reverse("accounts:logout") + '">Logout</a>',
        )
        self.assertContains(response, user.get_full_name())
