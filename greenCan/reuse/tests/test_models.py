from django.test import TestCase
from model_bakery import baker
from recycle.models import ZipCode
from reuse.models import Post, Image


class TestModels(TestCase):
    def test_Post_model(self):
        post = baker.make('reuse.Post')
        self.assertIsInstance(post,Post)

    def test_Image_model(self):
        image = baker.make('reuse.Image')
        self.assertIsInstance(image,Image)
        
    