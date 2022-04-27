from django.conf import settings
from django.contrib.auth import get_user_model, get_user
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.core import mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from accounts.models import LoginAttempt
from accounts.token import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from reuse.models import Post
from recycle.models import ZipCode
from rewards.models import EarnGreenCredits, ImageMeta, Event, CreditsLookUp


User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:create")

    def test_unauthenticated_user(self):
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        expected_url = reverse("home:index")
        self.assertRedirects(response, expected_url, 302)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "accounts/templates/signup.html")

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_method_with_valid_data(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "password1",
            "first-name": "john",
            "last-name": "doe",
        }
        response = self.client.post(self.url, data, follow=True)
        user = response.context["user"]
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = account_activation_token.make_token(user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Activate your account")
        self.assertEqual(
            mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL
        )  # change to your email <youremail>
        self.assertEqual(mail.outbox[0].to, ["testuser@gmail.com"])  # self.user.email
        self.assertEqual(
            mail.outbox[0].body,
            f"\nHi { user.get_full_name() },\n\nWe need to verify that you "
            "are the owner of this email address."
            "\n\nPlease click on the link to confirm your registration.\n"
            "http://example.com/accounts/activate/" + str(uid) + "/" + str(token) + "/\n\n",
        )

        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "success")
        self.assertEquals(
            message.message,
            "We have sent you an activation link in your email. Please confirm "
            "your email to continue. Check your spam folder if you don't receive it",
        )

    def test_post_method_with_invalid_data_1(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "password1",
            "first-name": "",
            "last-name": "doe",
        }
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "First name is required")

    def test_post_method_with_invalid_data_2(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "password1",
            "first-name": "john",
            "last-name": "",
        }
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Last name is required")

    def test_post_method_with_invalid_data_3(self):
        data = {
            "email": "",
            "password": "password1",
            "first-name": "john",
            "last-name": "doe",
        }
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Email is required")

    def test_post_method_with_invalid_data_4(self):
        data = {
            "email": "testuser@gmail.com",
            "password": "",
            "first-name": "john",
            "last-name": "doe",
        }
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Password is required")

    def test_post_method_with_duplicate_email(self):

        """
        Test to check if a user tries to register with a duplicate
        email the message should say user already exists
        """
        data = {
            "email": "nyc.greencan@gmail.com",
            "password": "random",
            "first-name": "john",
            "last-name": "doe",
        }
        response = self.client.post(self.url, data, follow=True)
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "User already exists")

    def test_csrf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestActivateAccountView(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="testuser@gmail.com",
            password="password",
            first_name="john",
            last_name="doe",
            is_active=False,
        )

    def test_test_with_valid_token(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))
        token = account_activation_token.make_token(self.user)

        url = reverse("accounts:activate", args=[uidb64, token])

        response = self.client.get(url, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, reverse("accounts:login"), 302)
        self.assertEquals(message.tags, "success")
        self.assertEquals(
            message.message,
            "Thank you for confirming your email. You can now login.",
        )

        user = User.objects.get(id=self.user.id)

        self.assertTrue(user.is_active)  # user status updated to active

    def test_with_invalid_token(self):
        uidb64 = urlsafe_base64_encode(force_bytes(3))  # user with id = 3 DoesNotExist
        token = account_activation_token.make_token(self.user)
        url = reverse("accounts:activate", args=[uidb64, token])

        response = self.client.get(url, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, reverse("accounts:login"), 302)
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Activation link is invalid!")


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
            is_active=True,
        )
        self.user2 = User.objects.create_user(
            email="testemail2@gmail.com",
            password="password2",
            first_name="jane",
            last_name="doe",
            is_active=False,
        )
        self.url = reverse("accounts:login")

    def test_message_login_is_required(self):
        response = self.client.get(self.url + "?next=/reuse/create-post")
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Login is required to access.")

    def test_unauthenticated_user_is_redirected(self):
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        expected_url = reverse("home:index")  # change expected_url in your project
        self.assertRedirects(response, expected_url, 302)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "accounts/templates/login.html"
        )  # change to your login template

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_method_with_valid_credentials(self):
        # user with these credentials exists and is active
        self.client.login(email="testemail@gmail.com", password="password1")
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_post_method_with_valid_credentials_redirect(self):
        data = {
            "email": "testemail@gmail.com",
            "password": "password1",
        }  # user with these credentials doesn't exist
        response = self.client.post(self.url, data, follow=True)
        user = get_user(self.client)
        login_attempt = LoginAttempt.objects.get(user=user)
        self.assertEquals(login_attempt.login_attempts, 0)
        self.assertRedirects(response, reverse("home:index"), 302)

    def test_with_invalid_credentials(self):
        data = {
            "email": "email@gmail.com",
            "password": "somepassword",
        }  # user with these credentials doesn't exist
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Incorrect email or password")

    def test_post_method_with_invalid_data_email(self):
        data = {"email": "", "password": "password1"}
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Email is required")

    def test_post_method_with_invalid_data_password(self):
        data = {"email": "testuser@gmail.com", "password": ""}
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Password is required")

    def test_inactive_user_cannot_login(self):
        # user with these credentials is_active = False
        data = {"email": self.user2.email, "password": self.user2.password}
        response = self.client.post(self.url, data, follow=True)
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Please verify your email first.")

    def test_login_attempts_increments_on_wrong_password(self):
        data = {
            "email": "testemail@gmail.com",
            "password": "passwordxxx",
        }  # wrong password
        self.client.post(self.url, data, follow=True)
        login_attempt = LoginAttempt.objects.get(user=self.user)
        self.assertEquals(
            login_attempt.login_attempts, 1
        )  # login attempt is created and incremented to 1

    def test_user_cannot_login_on_maximum_login_attempts_reach(self):
        LoginAttempt.objects.create(user=self.user, login_attempts=4)
        data = {
            "email": "testemail@gmail.com",
            "password": "passwordxxx",
        }  # wrong password
        self.client.post(self.url, data, follow=True)
        login_attempt = LoginAttempt.objects.get(user=self.user)
        self.assertEquals(login_attempt.login_attempts, 5)
        user = User.objects.get(id=self.user.id)  # is same as self.user
        self.assertFalse(user.is_active)

    def test_email_sent_on_maximum_reach(self):
        LoginAttempt.objects.create(user=self.user, login_attempts=4)
        data = {
            "email": "testemail@gmail.com",
            "password": "passwordxxx",
        }  # wrong password
        response = self.client.post(
            self.url, data, follow=True
        )  # after this post, user will be inactive & email sent

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Account suspended")
        self.assertEqual(
            mail.outbox[0].from_email, settings.EMAIL_HOST_USER
        )  # change to your email <youremail>
        self.assertEqual(mail.outbox[0].to, ["testemail@gmail.com"])  # self.user.email
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Account suspended, maximum login attempts exceeded. "
            "Reactivation link has been sent to your email",
        )

    def test_csrf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="testemail@gmail.com", password="password1")
        self.url = reverse("accounts:logout")

    def test_logout(self):
        # auth_user = authenticate('testemail@gmail.com','password1')
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        expected_url = reverse("accounts:login")
        self.assertRedirects(response, expected_url, 302)

        user = User.objects.get(id=self.user.id)
        self.assertNotIn(
            user.id, self.client.session
        )  # user does not have an active session i.e. is logged out


class TestForgetPassword(TestCase):
    def setUp(self):
        self.password_reset_sent_url = reverse_lazy("accounts:password-reset-sent")
        self.url = reverse_lazy("accounts:forget-password")
        self.testemail1 = "testemail@gmail.com"
        self.testemail2 = "testemail2@gmail.com"
        self.user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))

    def test_forget_password_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "accounts/templates/forget-password.html")
        self.assertEquals(response.status_code, 200)

    def test_forget_password_with_valid_data(self):
        data = {"email": self.testemail1}
        response = self.client.post(self.url, data, follow=True)
        token = PasswordResetTokenGenerator().make_token(self.user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Password reset for greenCan")
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to, [self.user.email])

        self.assertEqual(
            mail.outbox[0].body,
            render_to_string(
                "email/email-forgot-password.html",
                {
                    "user": self.user,
                    "domain": "example.com",
                    "uid": str(self.uidb64),
                    "token": str(token),
                },
            ),
        )
        self.assertRedirects(response, self.password_reset_sent_url, 302)

    def test_forget_password_with_invalid_data(self):
        data = {"email": self.testemail2}
        response = self.client.post(self.url, data, follow=True)
        self.assertFalse(response.context["form"].is_valid())

    def test_csrf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestPasswordResetDone(TestCase):
    def test_template_used(self):
        url = reverse_lazy("accounts:password-reset-complete")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "accounts/templates/reset-password-done.html")
        self.assertEquals(response.status_code, 200)


class TestPasswordResetSent(TestCase):
    def test_template_used(self):
        url = reverse_lazy("accounts:password-reset-sent")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "accounts/templates/forget-password-done.html")
        self.assertEquals(response.status_code, 200)


# testing profile
class TestUserProfile(TestCase):
    def setUp(self):
        user = User.objects.create(
            first_name="first1",
            last_name="last1",
            email="user1@gmail.com",
            password="password1",
            is_active=True,
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        self.url = reverse("accounts:user-profile")
        self.data = {"first_name": "first2", "last_name": "last2"}
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
        self.zipcode = zipcode

    def test_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "accounts/templates/user-profile.html")

    def test_info_changed_after_edit_profile(self):
        response = self.client.post(self.url, self.data, follow=True)
        user1 = get_user(self.client)
        self.assertEquals(user1.first_name, "first2")
        self.assertEquals(user1.last_name, "last2")
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "success")
        self.assertEquals(message.message, "Your details have been updated successfully")
        self.assertRedirects(response, self.url, 302)

    def test_info_changed_after_edit_profile_wrong_details_firstname(self):
        data = self.data.copy()
        data["first_name"] = ""
        response = self.client.post(self.url, data, follow=True)
        user1 = get_user(self.client)
        self.assertEquals(user1.first_name, "first1")
        self.assertEquals(user1.last_name, "last1")
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "First name is required")
        self.assertRedirects(response, self.url, 302)

    def test_info_changed_after_edit_profile_wrong_details_lastname(self):
        data = self.data.copy()
        data["last_name"] = ""
        response = self.client.post(self.url, data, follow=True)
        user1 = get_user(self.client)
        self.assertEquals(user1.first_name, "first1")
        self.assertEquals(user1.last_name, "last1")
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Last name is required")
        self.assertRedirects(response, self.url, 302)

    def test_info_changed_after_edit_profile_valid_zipcode(self):
        data = self.data.copy()
        data["zipcode"] = self.zipcode.zip_code
        response = self.client.post(self.url, data, follow=True)
        user1 = get_user(self.client)
        self.assertEquals(user1.first_name, "first2")
        self.assertEquals(user1.last_name, "last2")
        self.assertEquals(user1.zipcode, self.zipcode)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "success")
        self.assertEquals(message.message, "Your details have been updated successfully")
        self.assertRedirects(response, self.url, 302)

    def test_info_changed_after_edit_profile_invalid_zipcode(self):
        data = self.data.copy()
        data["zipcode"] = "9oi0"
        response = self.client.post(self.url, data, follow=True)
        user1 = get_user(self.client)
        self.assertEquals(user1.first_name, "first1")
        self.assertEquals(user1.last_name, "last1")
        self.assertEquals(user1.zipcode, None)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(message.message, "Please enter a valid 5 digit NYC zipcode")
        self.assertRedirects(response, self.url, 302)

    def test_info_changed_after_edit_profile_invalid_phone_number(self):
        data = self.data.copy()
        data["phone_number"] = "89hiuu9yp]["
        response = self.client.post(self.url, data, follow=True)
        user1 = get_user(self.client)
        self.assertEquals(user1.first_name, "first1")
        self.assertEquals(user1.last_name, "last1")
        self.assertEquals(user1.phone_number, None)
        self.assertEquals(user1.zipcode, None)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "error")
        self.assertEquals(
            message.message,
            "Please enter a valid 10 digit phone number. "
            "Just include numbers without country code or any special symbols.",
        )
        self.assertRedirects(response, self.url, 302)

    def test_info_changed_after_edit_profile_valid_phone_number(self):
        data = self.data.copy()
        data["phone_number"] = "8887776665"
        response = self.client.post(self.url, data, follow=True)
        user1 = get_user(self.client)
        self.assertEquals(user1.first_name, "first2")
        self.assertEquals(user1.last_name, "last2")
        self.assertEquals(user1.phone_number, data["phone_number"])
        self.assertEquals(user1.zipcode, None)
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "success")
        self.assertEquals(message.message, "Your details have been updated successfully")
        self.assertRedirects(response, self.url, 302)

    def test_csrf_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")


class TestUserProfileAvatar(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="first2",
            last_name="last2",
            email="user2@gmail.com",
            password="password2",
            avatar="1.svg",
            is_active=True,
        )
        self.url1 = reverse("accounts:user-profile")
        self.url2 = reverse("accounts:user-profile-avatar")

    def test_login_required(self):
        response = self.client.get(self.url2)
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + self.url2, 302)

    def test_returns_302(self):
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url2)
        self.assertRedirects(response, self.url1, 302)

    def test_info_changed_after_edit_profile_avatar(self):
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.post(self.url2, {"avatar": "2.svg"}, follow=True)
        user2 = get_user(self.client)
        self.assertEquals(user2.avatar, "2.svg")
        message = list(response.context.get("messages"))[0]
        self.assertEquals(message.tags, "success")
        self.assertEquals(message.message, "Your avatar has been updated.")


class TestUserGreenCreditLogs(TestCase):
    def setUp(self):

        CreditsLookUp.objects.create(action="post", credit=10)

        CreditsLookUp.objects.create(action="image", credit=5)

        self.user_1 = User.objects.create(
            first_name="first1", last_name="last1", email="user1@gmail.com", password="password1"
        )

        self.user_2 = User.objects.create(
            first_name="first2", last_name="last2", email="user2@gmail.com", password="password2"
        )

        zipcode = ZipCode.objects.create(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )

        post_1 = Post.objects.create(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="user1@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=self.user_1,
        )

        post_2 = Post.objects.create(
            title="Apple",
            category="Books",
            phone_number="1234567890",
            email="user2@nyu.edu",
            zip_code=zipcode,
            description=" Book on apple",
            user=self.user_2,
        )

        event = Event.objects.create(name="Recycle")

        image_meta_1 = ImageMeta.objects.create(
            event_type=event,
            location=zipcode,
            caption="This is a caption",
            user=self.user_1,
            consent=True,
        )

        self.log_1 = EarnGreenCredits.objects.create(
            content_object=post_1,
            action=CreditsLookUp.objects.get(action="post"),
            user=post_1.user,
            object_id=post_1.id,
        )

        self.log_2 = EarnGreenCredits.objects.create(
            content_object=post_2,
            action=CreditsLookUp.objects.get(action="post"),
            user=post_2.user,
            object_id=post_2.id,
        )

        self.log_3 = EarnGreenCredits.objects.create(
            content_object=image_meta_1,
            action=CreditsLookUp.objects.get(action="image"),
            user=image_meta_1.user,
            object_id=image_meta_1.id,
        )
        self.url = reverse("accounts:green-credits-logs") + "?page=1"
        self.url2 = reverse("accounts:user-profile")

    def test_green_credit_logs_login_required(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + self.url)

    def test_green_credit_logs_GET_1(self):
        self.client.force_login(self.user_1, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertJSONEqual(
            force_str(response.content),
            {
                "status": True,
                "next_page_number": 0,
                "data": [
                    {
                        "date": self.log_3.earned_on.strftime("%d %b' %Y - %I:%M:%S %p"),
                        "event_type": self.log_3.action.action,
                        "credits": self.log_3.action.credit,
                    },
                    {
                        "date": self.log_1.earned_on.strftime("%d %b' %Y - %I:%M:%S %p"),
                        "event_type": self.log_1.action.action,
                        "credits": self.log_1.action.credit,
                    },
                ],
            },
        )

    def test_green_credit_logs_GET_2(self):
        self.client.force_login(self.user_2, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        self.assertJSONEqual(
            force_str(response.content),
            {
                "status": True,
                "next_page_number": 0,
                "data": [
                    {
                        "date": self.log_2.earned_on.strftime("%d %b' %Y - %I:%M:%S %p"),
                        "event_type": self.log_2.action.action,
                        "credits": self.log_2.action.credit,
                    }
                ],
            },
        )

    def test_user_rank(self):
        self.client.force_login(self.user_1, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url2)
        self.assertEqual(response.context["rank"], 1)
        self.assertEqual(response.context["earned_credits"], 15)

    def test_new_user_rank(self):
        user = User.objects.create(
            email="newuser@gmail.com",
            password="newpassword",
            first_name="new",
            last_name="Sun",
        )
        self.client.force_login(user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url2)
        self.assertEqual(response.context["rank"], "Not Available")
        self.assertEqual(response.context["earned_credits"], 0)
