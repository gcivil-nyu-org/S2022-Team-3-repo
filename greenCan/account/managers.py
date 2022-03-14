from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


class UserManager(UserManager):
    """
    User model manager where email is the unique identifiers
    for authentication instead of username.
    """

    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        if not first_name:
            raise ValueError(_("The First name must be set"))
        if not last_name:
            raise ValueError(_("The Last name must be set"))
        if not password:
            raise ValueError(_("The Password must be set"))

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is True:
            raise ValueError(_("User must have is_staff=False"))
        if extra_fields.get("is_superuser") is True:
            raise ValueError(_("User must have is_superuser=False"))

        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self._create_user(email, first_name, last_name, password, **extra_fields)
