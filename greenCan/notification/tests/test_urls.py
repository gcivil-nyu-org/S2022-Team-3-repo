from django.test import TestCase
from notification.views import index, get_notifications
from django.urls import reverse, resolve


class TestNotificationUrls(TestCase):
    def test_index_URL(self):
        url = reverse("notification:index")
        self.assertEquals(resolve(url).func, index)
        self.assertEquals(resolve(url).namespace, "notification")
        self.assertEquals(url, "/notification/")

    def test_get_notifications_URL(self):
        url = reverse("notification:get-notifications")
        self.assertEquals(resolve(url).func, get_notifications)
        self.assertEquals(resolve(url).namespace, "notification")
        self.assertEquals(url, "/notification/get-notifications/")
