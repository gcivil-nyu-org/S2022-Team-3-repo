from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reuse.views import (
    index,
    donation_view,
    listing_page,
    create_post,
    my_posts,
    post_availability,
    post_details,
    raise_concerns,
)


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        """
        test index is resolved
        """
        url = reverse("reuse:index")
        self.assertEquals(resolve(url).func, index)
        self.assertEquals(resolve(url).namespace, "reuse")
        self.assertEquals(url, "/reuse/")

    def test_donationpage_url_is_resolved(self):
        """
        test donation page is resolved
        """
        url = reverse("reuse:donation-page")
        self.assertEquals(resolve(url).func, donation_view)
        self.assertEquals(resolve(url).namespace, "reuse")
        self.assertEquals(url, "/reuse/donations/")

    def test_listing_page_url_is_resolved(self):
        """
        test listing page is resolved
        """
        url = reverse("reuse:listing-page")
        self.assertEquals(resolve(url).func, listing_page)
        self.assertEquals(resolve(url).namespace, "reuse")
        self.assertEquals(url, "/reuse/listings/")

    def test_createpost_url_is_resolved(self):
        """
        test my posts page url is resolved
        """
        url = reverse("reuse:create-post")
        self.assertEquals(resolve(url).func, create_post)
        self.assertEquals(resolve(url).namespace, "reuse")
        self.assertEquals(url, "/reuse/create_post/")

    def test_my_posts_url(self):
        """
        test create post page url is resolved
        """
        url = reverse("reuse:my-posts")
        resolved = resolve(url)
        self.assertEqual(resolved.func, my_posts)
        self.assertEqual(resolved.namespace, "reuse")
        self.assertEqual(url, "/reuse/my-posts/")

    def test_post_availability_url(self):
        """
        test create post availability url is resolved
        """
        url = reverse("reuse:post-availability")
        resolved = resolve(url)
        self.assertEqual(resolved.func, post_availability)
        self.assertEqual(resolved.namespace, "reuse")
        self.assertEqual(url, "/reuse/post-availability/")

    def test_post_details_url(self):
        """
        test create post details url is resolved
        """
        url = reverse("reuse:post-details")
        resolved = resolve(url)
        self.assertEqual(resolved.func, post_details)
        self.assertEqual(resolved.namespace, "reuse")
        self.assertEqual(url, "/reuse/post-details/")

    def test_raise_concerns_url(self):
        """
        test create raise concerns url is resolved
        """
        url = reverse("reuse:raise-concerns")
        resolved = resolve(url)
        self.assertEqual(resolved.func, raise_concerns)
        self.assertEqual(resolved.namespace, "reuse")
        self.assertEqual(url, "/reuse/raise-concerns/")
