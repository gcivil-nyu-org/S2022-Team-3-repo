from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reuse.views import index, donation_view, listing_page, create_post


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("reuse:index")
        self.assertEquals(resolve(url).func, index)
        self.assertEquals(resolve(url).namespace, "reuse")
        self.assertEquals(url, "/reuse/")

    def test_donationpage_url_is_resolved(self):
        url = reverse("reuse:donation-page")
        self.assertEquals(resolve(url).func, donation_view)
        self.assertEquals(resolve(url).namespace, "reuse")
        self.assertEquals(url, "/reuse/donations/")

    def test_listingPage_url_is_resolved(self):
        url = reverse("reuse:listing-page")
        self.assertEquals(resolve(url).func, listing_page)
        self.assertEquals(resolve(url).namespace, "reuse")
        self.assertEquals(url, "/reuse/listings/")

    def test_createpost_url_is_resolved(self):
        url = reverse("reuse:create-post")
        self.assertEquals(resolve(url).func, create_post)
        self.assertEquals(resolve(url).namespace, "reuse")
        self.assertEquals(url, "/reuse/create_post/")
    
