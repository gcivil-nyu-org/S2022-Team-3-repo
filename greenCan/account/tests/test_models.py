from django.contrib.auth import get_user_model
from django.test import TestCase


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
        self.assertEquals(self.User.objects.get(id=1), user)

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
        self.assertEquals(self.User.objects.get(id=1), user)

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
        self.assertEquals(self.User.objects.get(id=1), user)
