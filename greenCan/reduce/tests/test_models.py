from django.test import TestCase
from model_bakery import baker
from reduce.models import RetailerLocation


class TestModels(TestCase):
    def test_RetailerLocation_model(self):
        retailer_location = baker.make("reduce.RetailerLocation")
        self.assertIsInstance(retailer_location, RetailerLocation)
        self.assertEquals(str(retailer_location), str(retailer_location.id))
