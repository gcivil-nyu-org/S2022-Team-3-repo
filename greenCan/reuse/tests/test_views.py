from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
from PIL import Image as Img
from six import BytesIO
from recycle.models import ZipCode
from reuse.models import Image, Post, NGOLocation, PostConcernLogs
from rewards.models import CreditsLookUp
from django.utils.encoding import force_str
from django.core import mail

User = get_user_model()


def create_image(storage, filename, size=(100, 100), image_mode="RGB", image_format="PNG"):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Img.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class TestCreatePost(TestCase):
    def setUp(self):
        self.url = reverse("reuse:create-post")
        self.redirect_url = reverse("reuse:donation-page")
        self.login_redirect_url = reverse("accounts:login") + "?next=" + self.url
        image = create_image(None, "test.png")
        image_file = SimpleUploadedFile("test.png", image.getvalue())
        image2 = create_image(None, "test2.png")
        image_file2 = SimpleUploadedFile("test2.png", image2.getvalue())
        self.data = {
            "file[]": [image_file, image_file2],
            "title": "Bed",
            "description": "Twin bed",
            "zipcode": "10001",
            "number": "9999999998",
            "email": "kevin@gmail.com",
            "category": "Furniture",
        }
        CreditsLookUp.objects.create(action="post", credit=10)
        zipcode = ZipCode(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )
        zipcode.save()

    def test_unauthenticated(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        self.assertRedirects(response, self.login_redirect_url, 302)
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)

    def test_auth_valid_form(self):
        data = self.data.copy()
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 1)
        images = Image.objects.all()
        self.assertEquals(len(images), 2)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "success")
        self.assertEquals(message.message, "Post created succesfully")
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_1(self):
        data = self.data.copy()
        del data["title"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Failed to create the post. Please make sure you fill"
            + " in all the details along with images to post an ad.",
        )
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_2(self):
        data = self.data.copy()
        del data["description"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Failed to create the post. Please make sure you fill"
            + " in all the details along with images to post an ad.",
        )
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_3(self):
        data = self.data.copy()
        del data["zipcode"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Failed to create the post. Please make sure you fill"
            + " in all the details along with images to post an ad.",
        )
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_4(self):
        data = self.data.copy()
        del data["category"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Failed to create the post. Please make sure you fill"
            + " in all the details along with images to post an ad.",
        )
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_5(self):
        data = self.data.copy()
        data["zipcode"] = "10002"
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Failed to create the post. Please make sure you fill"
            + " in all the details along with images to post an ad.",
        )
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_7(self):
        data = self.data.copy()
        del data["file[]"]
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Failed to create the post. Please make sure you fill"
            + " in all the details along with images to post an ad.",
        )
        self.assertRedirects(response, self.redirect_url, 302)

    def test_auth_invalid_form_8(self):
        data = self.data.copy()
        data["number"] = "999"
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url, data=data, follow=True)
        self.assertContains(response, "csrfmiddlewaretoken")
        posts = Post.objects.all()
        self.assertEquals(len(posts), 0)
        images = Image.objects.all()
        self.assertEquals(len(images), 0)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Failed to create the post. Please make sure you fill"
            + " in all the details along with images to post an ad.",
        )
        self.assertRedirects(response, self.redirect_url, 302)


class TestViews(TestCase):
    def setUp(self):
        self.index_url = reverse("reuse:index")
        self.donation_page_url = reverse("reuse:donation-page")
        self.listing_page_url = reverse("reuse:listing-page")
        self.create_post_url = reverse("reuse:create-post")
        self.ngo_location_url = reverse("reuse:ngo-donation")
        self.search_ngo_locations_url = reverse("reuse:fetch-ngo-locations")
        self.client = Client()
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])

        zipcode = ZipCode(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )
        zipcode.save()
        post = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="pb2640@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=user,
        )
        post.save()
        self.zipcode = zipcode
        ngo_location = NGOLocation(
            zip_code=zipcode,
            latitude=40.75021293296376,
            longitude=-73.99692994900218,
            items_accepted="Food",
            email="tandon@nyu.edu",
            phone="2121112011",
            address="101 Willoughby street",
            hours="Open on everyday",
            website="www.recycle.com",
        )
        ngo_location.save()
        self.ngo_location = ngo_location

    def test_index_GET(self):
        """
        test to check if reuse home page is returning a valid response
        """

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse-index.html")

    def test_donationpage_GET(self):
        """
        test to check if donation page is returning a valid response
        """

        response = self.client.get(self.donation_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse/templates/donate-item-page.html")

    def test_listing_page_GET(self):
        """
        test to check if listing page is returning a valid response
        """

        response = self.client.get(self.listing_page_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "listing-page.html")

    def test_listing_page_search_GET(self):
        """
        test to check if search is returning a valid response
        """
        response = self.client.get("%s?q=%s" % (reverse("reuse:listing-page"), "book"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "listing-page.html")
        self.assertEquals(len(response.context["q"]), len("book"))

    def test_listing_page_search_trim_more_characters(self):
        """
        test to check if search trimed to 256 characters
        """
        q = "a" * 1000
        response = self.client.get("%s?q=%s" % (reverse("reuse:listing-page"), q))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context["q"]), 256)

    def test_ngo_location_GET(self):
        """
        test to check if ngo page is returning a valid response
        """

        response = self.client.get(self.ngo_location_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse/templates/ngo-donation.html")

    def test_query_search_context_filter(self):
        """
        Test to check if on making a query something is being returned to the view
        """

        response = self.client.get("%s?q=%s" % (reverse("reuse:listing-page"), "book"))

        self.assertTrue(len(response.context["posts"]) >= 0)

    def test_query_search_returns(self):
        """
        Test to check if I search for an item which is present, it should return something
        """

        response = self.client.get("%s?q=%s" % (reverse("reuse:listing-page"), "book"))

        self.assertTrue(len(response.context["posts"]) >= 1)

    def test_query_search_does_not_return(self):
        """
        Test to check if I search for an item which is not present, it should return nothing
        """

        response = self.client.get("%s?q=%s" % (reverse("reuse:listing-page"), "veryrandomstring"))

        self.assertTrue(len(response.context["posts"]) == 0)

    def test_ngo_locations1(self):
        """
        test to check if searching by input zip code is returning a valid response
        """

        response = self.client.get(
            self.search_ngo_locations_url
            + "?type=live-location&latitude=40.7362&longitude=-74.0422"
        )

        self.assertEquals(response.status_code, 200)

    def test_ngo_locations2(self):
        """
        test to check if searching by input zip code is returning a valid response
        """

        response = self.client.get(self.search_ngo_locations_url + "?type=zipcode&zipcode=10001")

        self.assertEquals(response.status_code, 200)

    def test_ngo_locations_invalid_zip_code(self):
        """
        test to check if searching by an invalid zip code is returning a correct error message
        """

        response = self.client.get(self.search_ngo_locations_url + "?type=zipcode&zipcode=10004")

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            force_str(response.content),
            {"err_flag": True, "err_msg": "Please enter a valid NYC zip code"},
        )

    def test_ngo_locations_invalid_data(self):
        """
        test to check if searching by unknown type is returning a correct error message
        """

        response = self.client.get(self.search_ngo_locations_url + "?type=somerandomstring")

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            force_str(response.content),
            {"err_flag": True, "err_msg": "Invalid arguments provided"},
        )


class TestUserPostsViews(TestCase):
    def setUp(self):
        self.my_posts_url = reverse("reuse:my-posts")
        self.post_availability_url = reverse("reuse:post-availability")
        self.user = User.objects.create(
            first_name="first1",
            last_name="last1",
            email="user1@gmail.com",
            password="password1",
            is_active=True,
        )

        self.user2 = User.objects.create(
            first_name="first2",
            last_name="last2",
            email="user2@gmail.com",
            password="password2",
            is_active=True,
        )
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])

        self.admin = User.objects.create(
            email=settings.EMAIL_HOST_USER,
            password="newpassword",
            first_name="new",
            last_name="sun",
            admin=True,
        )

        zipcode = ZipCode(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )
        zipcode.save()
        self.post = Post(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="user1@gmail.com",
            zip_code=zipcode,
            description=" Book on apple",
            user=self.user,
        )
        self.post.save()
        self.zipcode = zipcode

        self.post_details_url = reverse("reuse:post-details")
        self.raise_concerns_url = reverse("reuse:raise-concerns")

        self.post2 = Post(
            title="Pear",
            category="Books",
            phone_number="1234567891",
            email="user2@gmail.com",
            zip_code=zipcode,
            description=" Book on pear",
            user=self.user2,
        )
        self.post2.save()

        self.post3 = Post(
            title="Apple3",
            category="Books",
            phone_number="9175185345",
            email="user@nyu.edu",
            zip_code=self.zipcode,
            description="Book on apple",
            user=self.user,
            approved=False,
        )
        self.post3.save()

    def test_my_posts_GET(self):
        """
        test to check if user posts page is returning a valid response
        """

        response = self.client.get(self.my_posts_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse/templates/my-posts.html")

    def test_post_availability_redirect(self):
        """
        test to check if the change of post availability is returning a valid response
        """
        response = self.client.get(self.post_availability_url)
        self.assertRedirects(response, self.my_posts_url, 302)

    def test_csrf_token(self):
        response = self.client.get(self.my_posts_url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_info_changed_after_change_availability_to_False(self):
        response = self.client.post(
            self.post_availability_url,
            {
                "id": self.post.id,
                "still_available": "false",
            },
            follow=True,
        )
        post = Post.objects.filter(id=self.post.id)[0]
        self.assertEquals(post.still_available, False)
        self.assertJSONEqual(force_str(response.content), {"message": "Success"})

    def test_info_changed_after_change_availability_to_True(self):
        response = self.client.post(
            self.post_availability_url,
            {
                "id": self.post.id,
                "still_available": "true",
            },
            follow=True,
        )
        post = Post.objects.filter(id=self.post.id)[0]
        self.assertEquals(post.still_available, True)
        self.assertJSONEqual(force_str(response.content), {"message": "Success"})

    def test_info_Invalid_Id(self):
        response = self.client.post(
            self.post_availability_url,
            {
                "id": 20,
                "still_available": "true",
            },
            follow=True,
        )
        self.assertJSONEqual(force_str(response.content), {"message": "Error"})

    def test_info_removed(self):
        post = Post(
            title="Apple",
            category="Books",
            phone_number="9175185345",
            email="user1@gmail.com",
            zip_code=self.zipcode,
            description=" Book on apple",
            user=self.user,
            approved=False,
        )
        post.save()
        response = self.client.post(
            self.post_availability_url,
            {
                "id": post.id,
                "still_available": "true",
            },
            follow=True,
        )
        self.assertJSONEqual(force_str(response.content), {"message": "Error"})

    def test_info_cannot_be_changed_by_other_user(self):
        post = Post(
            title="Apple",
            category="Books",
            phone_number="9175185345",
            email="user1@gmail.com",
            zip_code=self.zipcode,
            description=" Book on apple",
            user=self.user2,
        )
        post.save()
        response = self.client.post(
            self.post_availability_url,
            {
                "id": post.id,
                "still_available": "true",
            },
            follow=True,
        )
        self.assertJSONEqual(force_str(response.content), {"message": "Error"})

    # tests of post details
    def test_post_details_GET(self):
        """
        test to check if user get one post's detail is returning a valid response
        """
        response = self.client.get(
            self.post_details_url,
            {
                "postID": self.post.id,
            },
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reuse/templates/my-posts-details.html")

    def test_access_others_post_details_GET(self):
        """
        test to check if user can access other users' posts
        """
        response = self.client.get(
            self.post_details_url,
            {
                "postID": self.post2.id,
            },
        )
        self.assertEquals(response.status_code, 404)

    # tests of raise concerns
    def test_post_raise_concern_success(self):
        response = self.client.post(
            self.raise_concerns_url,
            {
                "id": self.post3.id,
            },
            follow=True,
        )
        self.assertJSONEqual(force_str(response.content), {"message": "Success"})
        self.assertEquals(len(PostConcernLogs.objects.all()), 1)

    def test_post_raise_concern_repeatly(self):
        self.client.post(
            self.raise_concerns_url,
            {
                "id": self.post3.id,
            },
            follow=True,
        )

        response = self.client.post(
            self.raise_concerns_url,
            {
                "id": self.post3.id,
            },
            follow=True,
        )
        self.assertJSONEqual(force_str(response.content), {"message": "Repeated"})
        self.assertEquals(len(PostConcernLogs.objects.all()), 1)

    def test_email_sent_to_admin(self):
        self.client.post(
            self.raise_concerns_url,
            {
                "id": self.post3.id,
            },
            follow=True,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "You have a new post concern to Review")
        self.assertEqual(
            mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL
        )  # change to your email <youremail>
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to, [settings.EMAIL_HOST_USER])  # self.user.email
        admin = User.objects.get(email=settings.EMAIL_HOST_USER)
        self.assertEqual(
            mail.outbox[0].body,
            f"\nHi { admin.get_full_name() },\n\n{ self.user.get_full_name() }"
            ", has raised a concern about his/her denied post."
            "\n\nYou can review it through the greenCan admin dashboard.\n\n\n\n",
        )
