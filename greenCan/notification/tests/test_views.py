from django.urls import reverse
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from notification.utils import create_notification
from django.utils import timezone


User = get_user_model()


class TestNotificationsViews(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            email="testemail1@gmail.com",
            password="password1",
            first_name="john1",
            last_name="doe1",
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

        self.url = reverse("notification:index")

        post = baker.make("reuse.Post")
        meta = baker.make("rewards.ImageMeta")

        create_notification(
            {
                "sender": self.user1,
                "receiver": self.user2,
                "msg_type": "success",
                "message": "Post was approved successfully",
                "notification_obj": post,
            }
        )

        create_notification(
            {
                "sender": self.user1,
                "receiver": self.user2,
                "msg_type": "error",
                "message": "Post was denied",
                "notification_obj": post,
            }
        )

        create_notification(
            {
                "sender": self.user1,
                "receiver": self.user2,
                "msg_type": "success",
                "message": "Image was approved successfully",
                "notification_obj": meta,
            }
        )

        create_notification(
            {
                "sender": self.user2,
                "receiver": self.user1,
                "msg_type": "success",
                "message": "Image was approved successfully",
                "notification_obj": meta,
            }
        )

        self.url_get_notifications = reverse("notification:get-notifications")

    def test_unauthenticated_users_GET(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("accounts:login") + f"?next={self.url}", 302)

    def test_template_used(self):
        self.client.force_login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "notification/templates/notification-index.html")

    def test_authenticated_users_GET(self):
        self.client.force_login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_index_has_csrf_GET(self):
        self.client.force_login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_callback_id_present(self):
        self.client.force_login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertContains(response, "notify_api_url='/inbox/notifications/api/unread_count/'")

    def test_get_user_notifications_unauthenticated_GET(self):
        response = self.client.post(
            self.url_get_notifications, data={"page": 1, "max": 5}, enforce_csrf_checks=True
        )
        self.assertRedirects(
            response, reverse("accounts:login") + f"?next={self.url_get_notifications}", 302
        )

    def test_get_user_notifications_POST(self):
        self.client.force_login(self.user2, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(
            self.url_get_notifications, data={"page": 1, "max": 5}, enforce_csrf_checks=True
        )
        data = response.json()
        self.assertEquals(len(data), 2)
        self.assertTrue("has_next" in data)
        self.assertTrue("notification" in data)
        self.assertEquals(data["has_next"], 0)
        self.assertEquals(len(data["notification"]), 3)
        self.assertTrue("message_type" in data["notification"][0])
        self.assertTrue("is_read" in data["notification"][0])
        self.assertTrue("created_on_date" in data["notification"][0])
        self.assertTrue("messages" in data["notification"][0])
        self.assertFalse(data["notification"][0]["is_read"])
        self.assertFalse(data["notification"][1]["is_read"])
        self.assertFalse(data["notification"][2]["is_read"])
        self.assertEquals(
            data["notification"][0]["created_on_date"], timezone.now().strftime("%B %d, %Y")
        )
        self.assertEquals(
            data["notification"][1]["created_on_date"], timezone.now().strftime("%B %d, %Y")
        )
        self.assertEquals(
            data["notification"][2]["created_on_date"], timezone.now().strftime("%B %d, %Y")
        )

    def test_get_user_notifications_has_next_POST(self):
        self.client.force_login(self.user2, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(
            self.url_get_notifications, data={"page": 1, "max": 2}, enforce_csrf_checks=True
        )
        data = response.json()
        self.assertEquals(len(data), 3)
        self.assertTrue("has_next" in data)
        self.assertTrue("notification" in data)
        self.assertTrue("next_page_number" in data)
        self.assertEquals(data["has_next"], 1)
        self.assertEquals(data["next_page_number"], 2)
        self.assertEquals(len(data["notification"]), 2)
        self.assertTrue("message_type" in data["notification"][0])
        self.assertTrue("is_read" in data["notification"][0])
        self.assertTrue("created_on_date" in data["notification"][0])
        self.assertTrue("messages" in data["notification"][0])
        self.assertFalse(data["notification"][0]["is_read"])
        self.assertFalse(data["notification"][1]["is_read"])
        self.assertEquals(
            data["notification"][0]["created_on_date"], timezone.now().strftime("%B %d, %Y")
        )
        self.assertEquals(
            data["notification"][1]["created_on_date"], timezone.now().strftime("%B %d, %Y")
        )

    def test_marked_is_read_POST(self):
        self.client.force_login(self.user2, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(
            self.url_get_notifications, data={"page": 1, "max": 5}, enforce_csrf_checks=True
        )
        response = self.client.post(
            self.url_get_notifications, data={"page": 1, "max": 5}, enforce_csrf_checks=True
        )
        data = response.json()
        self.assertTrue(data["notification"][0]["is_read"])
        self.assertTrue(data["notification"][1]["is_read"])
        self.assertTrue(data["notification"][2]["is_read"])

    def test_correct_count_of_notification_1_POST(self):
        self.client.force_login(self.user1, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(
            self.url_get_notifications, data={"page": 1, "max": 5}, enforce_csrf_checks=True
        )
        data = response.json()
        self.assertEquals(len(data), 2)
        self.assertTrue("has_next" in data)
        self.assertTrue("notification" in data)
        self.assertEquals(data["has_next"], 0)
        self.assertEquals(len(data["notification"]), 1)
        self.assertTrue("message_type" in data["notification"][0])
        self.assertTrue("is_read" in data["notification"][0])
        self.assertTrue("created_on_date" in data["notification"][0])
        self.assertTrue("messages" in data["notification"][0])
        self.assertFalse(data["notification"][0]["is_read"])

    def test_correct_count_of_notification_2_POST(self):
        self.client.force_login(self.user3, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(
            self.url_get_notifications, data={"page": 1, "max": 5}, enforce_csrf_checks=True
        )
        data = response.json()
        self.assertEquals(len(data), 2)
        self.assertTrue("has_next" in data)
        self.assertTrue("notification" in data)
        self.assertEquals(data["has_next"], 0)
        self.assertEquals(len(data["notification"]), 0)


class TestNotificationsApis(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="testemail1@gmail.com",
            password="password1",
            first_name="john1",
            last_name="doe1",
        )
        self.url = "/inbox/notifications/api/unread_count/?max=99"

    def test_notification_api_url_works_GET(self):
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
