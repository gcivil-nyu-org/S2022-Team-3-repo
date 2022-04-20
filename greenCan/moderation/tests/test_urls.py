from django.test import SimpleTestCase
from django.urls import reverse, resolve
from moderation.views import index, review_post


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
