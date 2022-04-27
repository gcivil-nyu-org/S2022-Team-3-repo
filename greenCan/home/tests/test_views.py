from django.conf import settings
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from rewards.models import EarnGreenCredits, CreditsLookUp, Event, ImageMeta
from recycle.models import ZipCode
from reuse.models import Post

User = get_user_model()


class TestHomePage(TestCase):
    def setUp(self):
        self.url = reverse_lazy("home:index")
        self.user1 = User.objects.create(
            email="testemail1@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )

        self.user2 = User.objects.create(
            email="testemail2@gmail.com",
            password="password2",
            first_name="john2",
            last_name="doe2",
        )
        self.user3 = User.objects.create(
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
        self.zipcode = zipcode

        post1 = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=self.user1,
        )
        post1.save()

        EarnGreenCredits.objects.create(
            object_id=post1.id,
            content_object=post1,
            action=CreditsLookUp.objects.get(action="post"),
            user=self.user1,
        )

        post2 = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=self.user2,
        )
        post2.save()

        EarnGreenCredits.objects.create(
            object_id=post2.id,
            content_object=post2,
            action=CreditsLookUp.objects.get(action="post"),
            user=self.user2,
        )

        post3 = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=self.user3,
        )
        post3.save()

        EarnGreenCredits.objects.create(
            object_id=post3.id,
            content_object=post3,
            action=CreditsLookUp.objects.get(action="post"),
            user=self.user3,
        )

        event = Event(name="Recycle")
        event.save()
        self.event = event

        meta1 = ImageMeta(
            caption="This is the caption!",
            event_type=event,
            location=zipcode,
            user=self.user1,
            consent=True,
        )
        meta1.save()

        meta2 = ImageMeta(
            caption="This is the caption!",
            event_type=event,
            location=zipcode,
            user=self.user2,
            consent=True,
        )
        meta2.save()

        meta3 = ImageMeta(
            caption="This is the caption!",
            event_type=event,
            location=zipcode,
            user=self.user1,
            consent=True,
        )
        meta3.save()

        EarnGreenCredits.objects.create(
            object_id=meta1.id,
            content_object=meta1,
            action=CreditsLookUp.objects.get(action="image"),
            user=self.user1,
        )

        EarnGreenCredits.objects.create(
            object_id=meta2.id,
            content_object=meta2,
            action=CreditsLookUp.objects.get(action="image"),
            user=self.user2,
        )

        EarnGreenCredits.objects.create(
            object_id=meta3.id,
            content_object=meta3,
            action=CreditsLookUp.objects.get(action="image"),
            user=self.user1,
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

    def test_unauthenticated_user_home_data(self):
        response = self.client.get(self.url)

        self.assertFalse("rank" in response.context)
        self.assertFalse("image_num" in response.context)
        self.assertFalse("image_meta_num" in response.context)
        self.assertFalse("post_num" in response.context)
        self.assertEqual(response.context["user1"], self.user1)
        self.assertEqual(response.context["user2"], self.user2)
        self.assertEqual(response.context["user3"], self.user3)
        self.assertEqual(response.context["gold"]["totalCredits"], 20)
        self.assertEqual(response.context["silver"]["totalCredits"], 15)
        self.assertEqual(response.context["bronze"]["totalCredits"], 10)

    def test_user_home_data_without_credits(self):
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )

        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertEqual(response.context["rank"], None)
        self.assertEqual(response.context["image_num"], 0)
        self.assertEqual(response.context["image_meta_num"], 0)
        self.assertEqual(response.context["post_num"], 0)
        self.assertEqual(response.context["user1"], self.user1)
        self.assertEqual(response.context["user2"], self.user2)
        self.assertEqual(response.context["user3"], self.user3)
        self.assertEqual(response.context["user"], user)
        self.assertEqual(response.context["gold"]["totalCredits"], 20)
        self.assertEqual(response.context["silver"]["totalCredits"], 15)
        self.assertEqual(response.context["bronze"]["totalCredits"], 10)

    def test_user_home_data_with_credits(self):
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        post1 = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=self.zipcode,
            description=" Book on apple",
            user=user,
        )
        post1.save()

        EarnGreenCredits.objects.create(
            object_id=post1.id,
            content_object=post1,
            action=CreditsLookUp.objects.get(action="post"),
            user=user,
        )

        post2 = Post(
            title="Apple1",
            category="Books1",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=self.zipcode,
            description="Book on apple",
            user=user,
        )
        post2.save()

        EarnGreenCredits.objects.create(
            object_id=post2.id,
            content_object=post2,
            action=CreditsLookUp.objects.get(action="post"),
            user=user,
        )

        meta = ImageMeta(
            caption="This is the caption!",
            event_type=self.event,
            location=self.zipcode,
            user=user,
            consent=True,
        )
        meta.save()

        EarnGreenCredits.objects.create(
            object_id=meta.id,
            content_object=meta,
            action=CreditsLookUp.objects.get(action="image"),
            user=user,
        )

        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)

        self.assertEqual(response.context["rank"], 1)
        self.assertEqual(response.context["image_num"], 0)
        self.assertEqual(response.context["image_meta_num"], 1)
        self.assertEqual(response.context["post_num"], 2)
        self.assertEqual(response.context["user1"], user)
        self.assertEqual(response.context["user2"], self.user1)
        self.assertEqual(response.context["user3"], self.user2)
        self.assertEqual(response.context["user"], user)
        self.assertEqual(response.context["gold"]["totalCredits"], 25)
        self.assertEqual(response.context["silver"]["totalCredits"], 20)
        self.assertEqual(response.context["bronze"]["totalCredits"], 15)
