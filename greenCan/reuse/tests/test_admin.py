from django.test import TestCase
from reuse.models import Post
from reuse.admin import PostAdmin

# from django.urls import reverse
from django.contrib.admin.sites import AdminSite

# from django.conf import settings


# def get_admin_change_view_url(obj: object) -> str:
#     return reverse(
#         'admin:{}_{}_change'.format(
#             obj._meta.app_label,
#             type(obj).__name__.lower()
#         ),
#         args=(obj.pk,)
#     )

# class TestPostConcernLogsAdmin(TestCase):
#     def setUp(self):
#         User = get_user_model()
#         user = User.objects.create(
#             email="user@gmail.com",
#             password="password1",
#             first_name="john",
#             last_name="doe",
#         )
#         self.user = user

#         self.admin = User.objects.create(
#             email="testemail@gmail.com",
#             password="password1",
#             first_name="john",
#             last_name="doe",
#             admin=True,
#         )

#         zipcode = ZipCode(
#             zip_code="10001",
#             state_id="NY",
#             state="New York",
#             borough="Manhattan",
#             centroid_latitude=40.75021293296376,
#             centroid_longitude=-73.99692994900218,
#             polygon="",
#         )
#         zipcode.save()
#         self.zipcode = zipcode

#         post = Post(
#             title="Apple",
#             category="Books",
#             phone_number="9175185345",
#             email="user1@gmail.com",
#             zip_code=self.zipcode,
#             description=" Book on apple",
#             user=self.user,
#             approved=False,
#         )
#         post.save()
#         self.post = post

#         post_concern = PostConcernLogs(post=self.post, checked=False, message="Approved!")
#         post_concern.save()
#         self.post_concern = post_concern
#         CreditsLookUp.objects.create(action="post", credit=10)

#         self.post_concern_log_admin = PostConcernLogsAdmin(PostConcernLogs, site)

#     def test_change_view(self):
#         self.client.force_login(self.admin, backend=settings.AUTHENTICATION_BACKENDS[0])
#         url = get_admin_change_view_url(self.post_concern)
#         response = self.client.get(url, follow=True)
#         self.assertIn(response.status_code, [200])
#         self.assertIs(response.resolver_match.func.__name__, "change_view")


class OurRequest(object):
    def __init__(self, user=None):
        self.user = user


class TestPostAdmin(TestCase):
    def setUp(self):
        self.postAdmin = PostAdmin(model=Post, admin_site=AdminSite())

    def test_has_add_permission(self):
        self.assertEquals(self.postAdmin.has_add_permission(OurRequest), False)

    def test_has_delete_permission(self):
        self.assertEquals(self.postAdmin.has_delete_permission(OurRequest), False)
