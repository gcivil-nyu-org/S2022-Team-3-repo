from django.test import TestCase
from model_bakery import baker
from ..models import VolunteerLogs


class TestModerationModels(TestCase):
    def test_log_model(self):
        log = baker.make("moderation.VolunteerLogs")
        self.assertIsInstance(log, VolunteerLogs)

    def test_log_model_str(self):
        log = baker.make("moderation.VolunteerLogs")
        self.assertEquals(str(log), str(log.id))

    # def test_log_model_property(self):
    #     log = baker.make("moderation.VolunteerLogs")
    #     log.approved = False
    #     log.save()
    #     self.assertEquals(log.is_approved(), False)
