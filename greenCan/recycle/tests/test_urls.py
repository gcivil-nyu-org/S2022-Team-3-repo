from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recycle.views import index, search_dropoff_locations


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("recycle:index")
        self.assertEquals(resolve(url).func, index)
        self.assertEquals(resolve(url).namespace, "recycle")
        self.assertEquals(url, "/recycle/")

    def test_fetchdropfflocations_url_is_resolved(self):
        url = reverse("recycle:fetch-drop-off-locations")
        self.assertEquals(resolve(url).func, search_dropoff_locations)
        self.assertEquals(resolve(url).namespace, "recycle")
        self.assertEquals(url, "/recycle/fetch-drop-off-locations")
