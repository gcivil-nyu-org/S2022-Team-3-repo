from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import index


class TestUrls(SimpleTestCase):
    def test_home_page_url(self):
        url = reverse("home:index")
        resolved = resolve(url)
        self.assertEqual(resolved.func, index)
        self.assertEqual(resolved.namespace, "home")
        self.assertEqual(url, "/")
