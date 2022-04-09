from django.test import TestCase
from helper.views import (
    error_400,
    error_403,
    error_404,
    error_405,
    error_500,
    error_502,
    ERROR_PAGE_TEMPLATE,
)
from django.test.client import RequestFactory

from greenCan import urls


class TestErrorPages(TestCase):
    def test_template_used(self):
        self.assertAlmostEquals(ERROR_PAGE_TEMPLATE, "helper/templates/error-page-template.html")

    def test_error_handlers_in_urls(self):
        self.assertTrue(urls.handler400.endswith(".error_400"))
        self.assertTrue(urls.handler405.endswith(".error_405"))
        self.assertTrue(urls.handler403.endswith(".error_403"))
        self.assertTrue(urls.handler404.endswith(".error_404"))
        self.assertTrue(urls.handler502.endswith(".error_502"))
        self.assertTrue(urls.handler500.endswith(".error_500"))

    def test_error_400(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = error_400(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("400", response.content.decode("utf-8"))

    def test_error_403(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = error_403(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn("403", response.content.decode("utf-8"))

    def test_error_404(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = error_404(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn("404", response.content.decode("utf-8"))

    def test_error_405(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = error_405(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn("405", response.content.decode("utf-8"))

    def test_error_500(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = error_500(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn("500", response.content.decode("utf-8"))

    def test_error_502(self):
        factory = RequestFactory()
        request = factory.get("/")
        response = error_502(request)
        self.assertEqual(response.status_code, 502)
        self.assertIn("502", response.content.decode("utf-8"))
