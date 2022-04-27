from django.test import TestCase
from moderation.models import VolunteerLogs
from model_bakery import baker


class TestModerationModels(TestCase):
    def test_volunteer_logs_model(self):
        volunteer_log = baker.make("moderation.VolunteerLogs")
        self.assertIsInstance(volunteer_log, VolunteerLogs)
