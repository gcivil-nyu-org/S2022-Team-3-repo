from django.test import TestCase
from model_bakery import baker
from recycle.models import ZipCode, DropOffLocation


class TestModels(TestCase):
    def test_Zipcode_model(self):
        zipcode = baker.make("recycle.ZipCode")
        self.assertIsInstance(zipcode, ZipCode)

    def test_DropOffLocation_model(self):
        dropoffloc = baker.make("recycle.DropOffLocation")
        self.assertIsInstance(dropoffloc, DropOffLocation)
        self.assertEquals(str(dropoffloc), str(dropoffloc.id))
