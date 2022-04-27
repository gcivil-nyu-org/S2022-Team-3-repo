from django.test import TestCase
from model_bakery import baker
from notification.models import Notification


class TestModels(TestCase):
    def test_Notification_model(self):
        notification = baker.make("notification.Notification")
        self.assertIsInstance(notification, Notification)
        self.assertEquals(str(notification), str(notification.id))
