from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.models import LoginAttempt


class TestModelManager(TestCase):
    def setUp(self):
        self.email = "user@gmail.com"
        self.password = "password1"
        self.first_name = "john"
        self.last_name = "doe"
        self.User = get_user_model()

    def test_createuser_method(self):
        user = self.User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.assertEquals(user.is_active, True)
        self.assertEquals(user.is_staff, False)
        self.assertEquals(user.is_admin, False)
        self.assertEquals(self.User.objects.get(id=user.id), user)

    def test_createuser_method_invalid_email(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email="",
                password=self.password,
                first_name=self.first_name,
                last_name=self.last_name,
            )

    def test_createuser_method_invalid_password(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email=self.email,
                password="",
                first_name=self.first_name,
                last_name=self.last_name,
            )

    def test_createuser_method_invalid_first_name(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email=self.email,
                password=self.password,
                first_name="",
                last_name=self.last_name,
            )

    def test_createuser_method_invalid_last_name(self):
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email=self.email,
                password=self.password,
                first_name=self.first_name,
                last_name="",
            )

    def test_createstaff_method(self):
        user = self.User.objects.create_staffuser(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.assertEquals(user.is_active, True)
        self.assertEquals(user.is_staff, True)
        self.assertEquals(user.is_admin, False)
        self.assertEquals(self.User.objects.get(id=user.id), user)

    def test_createsuperuser_method(self):
        user = self.User.objects.create_superuser(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.assertEquals(user.is_active, True)
        self.assertEquals(user.is_staff, True)
        self.assertEquals(user.is_admin, True)
        self.assertEquals(self.User.objects.get(id=user.id), user)


class TestUserModel(TestCase):
    def setUp(self):
        self.email = "user@gmail.com"
        self.password = "password1"
        self.first_name = "john"
        self.last_name = "doe"
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def test_str_wrapper(self):
        self.assertEquals(str(self.user), self.email)

    def test_get_full_name(self):
        self.assertEquals(
            self.user.get_full_name(),
            self.first_name.title() + " " + self.last_name.title(),
        )

    def test_has_perm(self):
        self.assertTrue(self.user.has_perm("SOME-PERMISSION"))

    def test_has_module_perms(self):
        self.assertTrue(self.user.has_module_perms("SOME-APP-LABEL"))


class TestLoginAttempt(TestCase):
    def setUp(self):
        self.email = "user@gmail.com"
        self.password = "password1"
        self.first_name = "john"
        self.last_name = "doe"
        self.User = get_user_model()

    def test_login_attempt_str(self):
        user = self.User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        login_attempt = LoginAttempt(user=user)

        self.assertEquals(str(login_attempt), f"user: {self.email}, attempts: {0}")
