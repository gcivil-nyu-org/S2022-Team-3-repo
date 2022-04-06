from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reduce.views import (
    index,
    search_retailer_locations,
)


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        """
        test index is resolved
        """
        url = reverse("reduce:index")
        self.assertEquals(resolve(url).func, index)
        self.assertEquals(resolve(url).namespace, "reduce")
        self.assertEquals(url, "/reduce/")

    def test_searching_url_is_resolved(self):
        """
        test searching function's url is resolved
        """
        url = reverse("reduce:fetch-retailer-locations")
        self.assertEquals(resolve(url).func, search_retailer_locations)
        self.assertEquals(resolve(url).namespace, "reduce")
        self.assertEquals(url, "/reduce/fetch-retailer-locations/")
