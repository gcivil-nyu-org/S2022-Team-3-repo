from django.test import TestCase
from model_bakery import baker
from rewards.models import Event, Image, Category, ImageMeta, CreditsLookUp, EarnGreenCredits


class TestModels(TestCase):
    def test_Category_model(self):
        category = baker.make("rewards.Category")
        self.assertIsInstance(category, Category)

    def test_Image_model(self):
        image = baker.make("rewards.Image")
        self.assertIsInstance(image, Image)

    def test_ImageMeta_model(self):
        image = baker.make("rewards.ImageMeta")
        self.assertIsInstance(image, ImageMeta)

    def test_Event_model(self):
        event = baker.make("rewards.Event")
        self.assertIsInstance(event, Event)

    def test_EarnGreenCredits_model(self):
        earnGreenCredits = baker.make("rewards.EarnGreenCredits")
        self.assertIsInstance(earnGreenCredits, EarnGreenCredits)

    def test_CreditsLookUp_model(self):
        creditsLookUp = baker.make("rewards.CreditsLookUp")
        self.assertIsInstance(creditsLookUp, CreditsLookUp)
