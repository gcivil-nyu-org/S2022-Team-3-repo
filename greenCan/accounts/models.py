from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from recycle.models import ZipCode


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        zipcode=None,
        phone_number=None,
        password=None,
        is_staff=False,
        is_admin=False,
        is_active=True,
    ):  # may look repetitive adding staff, admin and active status,
        # but it simplifies the
        # work when using create_staffuser() and create_superuser()
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            phone_number=phone_number,
            zipcode=zipcode,
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(
        self,
        email,
        first_name,
        last_name,
        zipcode=None,
        phone_number=None,
        password=None,
    ):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            zipcode=zipcode,
            phone_number=phone_number,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        zipcode=None,
        phone_number=None,
        password=None,
    ):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            zipcode=zipcode,
            phone_number=phone_number,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(verbose_name="First name", max_length=100, null=False)
    last_name = models.CharField(verbose_name="Last name", max_length=100, null=False)
    zipcode = models.ForeignKey(
        ZipCode, verbose_name="Zipcode", on_delete=models.CASCADE, null=True
    )
    phone_number = models.CharField(verbose_name="Phone number", max_length=17, null=True)
    avatar = models.TextField(verbose_name="Avatar", null=True)
    # avatar = models.ImageField(upload_to="Avatars", null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    # this now over rides the username
    # field and now email is the default field
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
    # if you add another field and need it to be required,
    # include it in the list

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_attempts = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "user: {}, attempts: {}".format(self.user.email, self.login_attempts)
