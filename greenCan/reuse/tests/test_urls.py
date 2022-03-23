from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reuse.views import index, donation_view, listing_page, create_post


class TestUrls(SimpleTestCase):
    def test_index(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)

    def test_donation_view(self):
        url = reverse("donation-page")
        self.assertEqual(resolve(url).func, donation_view)

    def test_listing_page(self):
        url = reverse("listingPage")
        self.assertEqual(resolve(url).func, listing_page)

    def test_create_post(self):
        url = reverse("create-post")
        self.assertEqual(resolve(url).func, create_post)
