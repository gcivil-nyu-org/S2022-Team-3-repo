from django.test import SimpleTestCase
from django.urls import reverse, resolve
from moderation.views import index, review_post, review_credit_request


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        """
        test index is resolved
        """
        url = reverse("moderation:index")
        self.assertEquals(resolve(url).func, index)
        self.assertEquals(resolve(url).namespace, "moderation")
        self.assertEquals(url, "/volunteer/")

    def test_review_post_url_is_resolved(self):
        """
        test review post is resolved
        """
        url = reverse("moderation:review-post", kwargs={"id": 1})
        self.assertEquals(resolve(url).func, review_post)
        self.assertEquals(resolve(url).namespace, "moderation")
        self.assertEquals(url, "/volunteer/review/post/1")

    def test_credit_post_url_is_resolved(self):
        """
        test credit post is resolved
        """
        url = reverse("moderation:review-credit", kwargs={"id": 1})
        self.assertEquals(resolve(url).func, review_credit_request)
        self.assertEquals(resolve(url).namespace, "moderation")
        self.assertEquals(url, "/volunteer/review/credit-request/1")
