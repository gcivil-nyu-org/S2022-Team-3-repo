from django.test import TestCase
from model_bakery import baker
from ..models import VolunteerLogs


class TestModerationModels(TestCase):
    def test_log_model(self):
        log = baker.make("moderation.VolunteerLogs")
        self.assertIsInstance(log, VolunteerLogs)
        self.assertEquals(str(log), str(log.id))
