from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from reuse.models import Post
from recycle.models import ZipCode
from django.core import mail

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


class TestReviewPost(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="testemail1@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
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
        post = Post(
            title="Apple",
            category="Books",
            phone_number="9175185345",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=user,
        )
        post.save()
        self.url_1 = reverse("moderation:review-post", kwargs={"id": post.id})
        self.url_2 = reverse("moderation:review-post", kwargs={"id": 2})

    def test_unauthenticated_user(self):
        """
        test to verify only authenticated user can access
        the rewards index page unauthenticated user must
        be redirected to the login page
        """
        response = self.client.get(self.url_1)
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + self.url_1, 302)

    def test_non_staff_cannot_access(self):
        """
        test non staff user cannot access this page
        """
        user = User.objects.create(
            email="testemail2@gmail.com",
            password="password2",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url_1)
        self.assertRedirects(
            response,
            reverse("accounts:login") + "?next=" + self.url_1,
            302,
            target_status_code=302,
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
        response = self.client.get(self.url_1)
        self.assertEquals(response.status_code, 200)

    def test_valid_url_1(self):
        """
        test post is valid and review page is returned
        """
        volunteer = User.objects.create(
            email="testemail@gmail.com", password="password1", first_name="john", last_name="doe"
        )
        volunteer.staff = True
        volunteer.save()
        self.client.force_login(volunteer, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url_1)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["post"].title, "Apple")
        self.assertEquals(response.context["post"].category, "Books")

    def test_template_used(self):
        """
        test valid template is used for review post
        """
        volunteer = User.objects.create(
            email="testemail@gmail.com", password="password1", first_name="john", last_name="doe"
        )
        volunteer.staff = True
        volunteer.save()
        self.client.force_login(volunteer, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url_1)
        self.assertTemplateUsed(response, "moderation/templates/review-post.html")


class TestSubmissionActions(TestCase):
    """
    1. use admin to take latest post and set it to unknown
    2. use a staffs account to
    """

    def setUp(self):
        self.user = User.objects.create(
            email="testemail1@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        zipcode = ZipCode(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )
        self.user.staff = True
        self.user.save()
        zipcode.save()
        self.post = Post(
            title="Apple",
            category="Books",
            phone_number="9175185345",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=self.user,
        )
        self.post.save()
        self.url = reverse("moderation:review-post", kwargs={"id": self.post.id})

    def test_post_approval_email_status(self):
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        data = {"approve": self.post.id}
        response = self.client.post(self.url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "moderation/templates/index.html")

    def test_post_approval_email_subject(self):
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        data = {"approve": self.post.id}
        self.client.post(self.url, data, follow=True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Post " + str(self.post.title) + " approved")

    def test_post_denial_email_response(self):
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        data = {"deny": self.post.id}
        response = self.client.post(self.url, data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "moderation/templates/index.html")

    def test_post_denial_email_subject(self):
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        data = {"deny": self.post.id, "check1": "check1 reason"}
        self.client.post(self.url, data, follow=True)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Post " + str(self.post.title) + " denied")
