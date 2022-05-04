from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from accounts.models import LoginAttempt, VolunteerApplication


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


class TestVolunteerApplication(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            email="user@gmail.com",
            password="password1",
            first_name="john",
            last_name="doe",
        )

        self.admin = User.objects.create(
            email="admin@gmail.com", password="password1", first_name="greencan", last_name="admin"
        )

    def test_is_instance(self):
        application = baker.make("accounts.VolunteerApplication")
        self.assertIsInstance(application, VolunteerApplication)

    def test_str_method(self):
        application = VolunteerApplication.objects.create(
            user=self.user,
            approved_by=self.admin,
            score=4,
            essay_1="This is essay 1",
            essay_2="This is essay 2",
        )
        applications = VolunteerApplication.objects.all()
        self.assertEquals(len(applications), 1)
        self.assertEquals(str(application), self.user.get_full_name())
        self.assertEquals(application.essay_1, "This is essay 1")
        self.assertEquals(application.essay_2, "This is essay 2")
        self.assertEquals(application.score, 4)
        self.assertEquals(application.approved_by, self.admin)
