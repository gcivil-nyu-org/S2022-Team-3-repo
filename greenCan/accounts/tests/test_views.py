from django.conf import settings
from django.contrib.auth import get_user_model, get_user
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.models import LoginAttempt
from accounts.token import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string


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
            mail.outbox[0].from_email, settings.EMAIL_HOST_USER
        )  # change to your email <youremail>
        self.assertEqual(mail.outbox[0].to, ["testuser@gmail.com"])  # self.user.email
        self.assertEqual(
            mail.outbox[0].body,
            f"\nHi { user.get_full_name() },\n\nWe need to verify that you are the owner of this email address."
            "\n\nPlease click on the link to confirm your registration.\n"
            "http://example.com/accounts/activate/"
            + str(uid)
            + "/"
            + str(token)
            + "/\n\n",
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
            message.message, "Thank you for confirming your email. You can now login."
        )

        user = User.objects.get(id=1)

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
        user = User.objects.get(id=1)  # is same as self.user
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
        self.user = User.objects.create(
            email="testemail@gmail.com", password="password1"
        )
        self.url = reverse("accounts:logout")

    def test_logout(self):
        # auth_user = authenticate('testemail@gmail.com','password1')
        self.client.force_login(self.user, backend=settings.AUTHENTICATION_BACKENDS[0])
        response = self.client.get(self.url)
        expected_url = reverse("accounts:login")
        self.assertRedirects(response, expected_url, 302)

        user = User.objects.get(id=1)
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
        self.assertTemplateUsed(
            response, "accounts/templates/forget-password-done.html"
        )
        self.assertEquals(response.status_code, 200)


# testing profile


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            first_name="user1_first",
            last_name="user1_last",
            email="user1@gmail.com",
            password="1234",
        )
        self.user2 = User.objects.create_user(
            first_name="user2_first",
            last_name="user2_last",
            email="user2@gmail.com",
            password="1234",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("accounts:user-profile", kwargs=({"email": self.user1.email}))
        )

        self.assertRedirects(response, "/accounts/login/?next=/accounts/user-profile")

    def test_returns_200(self):
        self.client.login(email="user1@gmail.com", password="1234")
        response = self.client.get(
            reverse("accounts:user-profile", kwargs=({"email": self.user1.email}))
        )

        self.assertEqual(response.status_code, 200)

    def test_view_returns_profile_of_current_user(self):
        self.client.login(email="user1@gmail.com", password="1234")
        response = self.client.get(
            reverse("accounts:user-profile", kwargs=({"email": self.user1.email}))
        )
        # Check we got the profile of the current user
        self.assertEqual(response.context["user"], self.user1)

    def test_view_returns_profile_of_a_given_user(self):
        self.client.login(email="user1@gmail.com", password="1234")
        # access the profile of the user 'user'
        response = self.client.get(
            reverse("accounts:user-profile", kwargs=({"email": self.user2.email}))
        )
        self.assertEqual(response.context["user"], self.user2)
