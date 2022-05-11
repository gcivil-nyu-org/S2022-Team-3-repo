from django.test import TestCase, RequestFactory
from model_bakery import baker
from reuse.models import Post, Image, NGOLocation, PostConcernLogs
from recycle.models import ZipCode
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rewards.models import CreditsLookUp


class TestModels(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        user = User.objects.create(
            email="user@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        user.save()
        self.user = user

        admin = User.objects.create(
            email="admin@gmail.com", password="password1", first_name="greencan", last_name="admin"
        )
        admin.save()
        self.admin = admin

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

        post = Post(
            title="Apple",
            category="Books",
            phone_number="9175185345",
            email="user1@gmail.com",
            zip_code=self.zipcode,
            description=" Book on apple",
            user=self.user,
            approved=False,
        )
        post.save()
        self.post = post

        post_concern = PostConcernLogs(post=self.post, checked=False, message="Approved!")
        self.post_concern = post_concern
        CreditsLookUp.objects.create(action="post", credit=10)

    def test_Post_model(self):
        post = baker.make("reuse.Post")
        self.assertIsInstance(post, Post)
        self.assertEquals(str(post), str(post.id))

    def test_Image_model(self):
        image = baker.make("reuse.Image")
        self.assertIsInstance(image, Image)
        self.assertEquals(str(image), str(image.id))

    def test_NGOLocation_model(self):
        ngo_location = baker.make("reuse.NGOLocation")
        self.assertIsInstance(ngo_location, NGOLocation)
        self.assertEquals(str(ngo_location), str(ngo_location.id))

    def test_PostConcernLogs_model(self):
        post_concern_logs = baker.make("reuse.PostConcernLogs")
        self.assertIsInstance(post_concern_logs, PostConcernLogs)
        self.assertEquals(str(post_concern_logs), str(post_concern_logs))

    def test_send_signals_and_moderate_for_approve_for_approve(self):
        url = reverse("home:index")
        request = self.factory.get(url)
        self.post_concern.send_signals_and_moderate(self.user, 1, get_current_site(request), "A")
        self.assertEquals(self.post_concern.checked, True)
        self.assertEquals(self.post_concern.post.approved, True)

    def test_send_signals_and_moderate_for_approve_for_reject(self):
        url = reverse("home:index")
        request = self.factory.get(url)
        self.post_concern.send_signals_and_moderate(self.user, 0, get_current_site(request), "R")
        self.assertEquals(self.post_concern.checked, True)
        self.assertEquals(self.post_concern.post.approved, False)
