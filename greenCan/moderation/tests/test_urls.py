from django.test import SimpleTestCase
from django.urls import reverse, resolve
from moderation.views import index


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        """
        test index is resolved
        """
        url = reverse("moderation:index")
        self.assertEquals(resolve(url).func, index)
        self.assertEquals(resolve(url).namespace, "moderation")
        self.assertEquals(url, "/volunteer/")
