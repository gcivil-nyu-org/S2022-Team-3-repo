from django.conf import settings
from django.contrib.auth import get_user_model, get_user
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from account.models import LoginAttempt
from account.token import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("account:create")

    def test_unauthenticated_user(self):
        user = User.objects.create(
            email="testemail@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )
        self.client._login(user)
        response = self.client.get(self.url)
        expected_url = reverse("home:index")
        self.assertRedirects(response, expected_url, 302)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "account/templates/signup.html")

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
            f"\nHi {data['first-name']+' '+data['last-name']},\nPlease click on the link to confirm your registration,\n"
            "http://testserver/account/activate/" + str(uid) + "/" + str(token) + "/\n",
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

        url = reverse("account:activate", args=[uidb64, token])

        response = self.client.get(url, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, reverse("account:login"), 302)
        self.assertEquals(message.tags, "success")
        self.assertEquals(
            message.message, "Thank you for confirming your email. You can now login."
        )

        user = User.objects.get(id=1)

        self.assertTrue(user.is_active)  # user status updated to active

    def test_with_invalid_token(self):
        uidb64 = urlsafe_base64_encode(force_bytes(3))  # user with id = 3 DoesNotExist
        token = account_activation_token.make_token(self.user)
        url = reverse("account:activate", args=[uidb64, token])

        response = self.client.get(url, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertRedirects(response, reverse("account:login"), 302)
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
        self.url = reverse("account:login")

    def test_unauthenticated_user_is_redirected(self):
        self.client._login(self.user)
        response = self.client.get(self.url)
        expected_url = reverse("home:index")  # change expected_url in your project
        self.assertRedirects(response, expected_url, 302)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "account/templates/login.html"
        )  # change to your login template

    def test_response_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post_method_with_valid_credentials(self):
        # user with these credentials exists and is active
        self.client.login(email="testemail@gmail.com", password="password1")
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

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

    def test_inactive_user_cannot_login(self):
        # user with these credentials is_active = False
        self.client.login(email="testemail2@gmail.com", password="password2")
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

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
        self.url = reverse("account:logout")

    def test_logout(self):
        self.client._login(self.user)
        response = self.client.get(self.url)
        expected_url = reverse("account:login")
        self.assertRedirects(response, expected_url, 302)

        user = User.objects.get(id=1)
        self.assertNotIn(
            user.id, self.client.session
        )  # user does not have an active session i.e. is logged out


class TestForgetPassword(TestCase):
    def setUp(self):
        self.password_reset_sent_url = reverse_lazy("account:password-reset-sent")
        self.url = reverse_lazy("account:forget-password")
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
        self.assertTemplateUsed(response, "account/templates/forget-password.html")
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
            f"\nHi {self.user.get_full_name()},\nForgot your password? Don't worry.\n\nClick the link below to reset your account password.\n"
            "http://testserver/account/reset/"
            + str(self.uidb64)
            + "/"
            + str(token)
            + "/\n",
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
        url = reverse_lazy("account:password-reset-complete")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "account/templates/reset-password-done.html")
        self.assertEquals(response.status_code, 200)


class TestPasswordResetSent(TestCase):
    def test_template_used(self):
        url = reverse_lazy("account:password-reset-sent")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "account/templates/forget-password-done.html")
        self.assertEquals(response.status_code, 200)


# class TestPasswordReset(TestCase):

#     def setUp(self):
#         self.url_str = "account:password-reset"
#         self.password_reset_done_url = reverse_lazy("account:password-reset-complete")
#         self.user = User.objects.create(
#             email="testemail@gmail.com",
#             password="password1",
#             first_name="john",
#             last_name="doe",
#         )
#         self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.id))

#     def test_template_used(self):
#         token = PasswordResetTokenGenerator().make_token(self.user)
#         response = self.client.get(reverse_lazy(self.url_str, args=[self.uidb64,token]))
#         self.assertTemplateUsed(response,'account/templates/reset-password.html')
#         self.assertEquals(response.status_code, 200)

#     def test_csrf_token(self):
#         token = PasswordResetTokenGenerator().make_token(self.user)
#         response = self.client.get(reverse_lazy(self.url_str, args=[self.uidb64,token]))
#         self.assertContains(response, "csrfmiddlewaretoken")

#     def test_password_reset_valid_data(self):
#         data = {
#             'password': 'newpassword1',
#             'confirm_password': 'newpassword2'
#         }
#         token = PasswordResetTokenGenerator().make_token(self.user)
#         response = self.client.post(reverse_lazy(self.url_str, args=[self.uidb64,token]), data, follow=True)
#         self.assertRedirects(response, self.password_reset_done_url, 302)

#     def test_password_reset_invalid_data_1(self):
#         data = {
#             'password': '',
#             'confirm_password': 'newpassword2'
#         }
#         token = PasswordResetTokenGenerator().make_token(self.user)
#         response = self.client.post(reverse_lazy(self.url_str, args=[self.uidb64,token]), data, follow=True)
#         self.assertRedirects(response, reverse_lazy(self.url_str, args=[self.uidb64,token]) , 302)
