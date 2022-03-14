from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    # add first_name, last_name, email, phone, address
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=17, null=True)
    email = models.EmailField(null=True)
    address = models.TextField(null=False)

    def __str__(self):
        return str(self.id)


# from django.contrib.auth.models import AbstractUser
# from .managers import UserManager
# from recycle.models import ZipCode
# from django.utils.translation import gettext_lazy as _

# class User(AbstractUser):
#     username = None
#     email = models.EmailField(_('email'),unique=True, max_length=255, null=False)
#     avatar = models.URLField(_('avatar'),max_length=2000, null=True)
#     first_name = models.CharField(_('first_name'),max_length=100, null=False)
#     last_name = models.CharField(_('last_name'),max_length=100, null=False)
#     phone_number = models.CharField(max_length=17, null=True)
#     zipcode = models.ForeignKey(ZipCode, on_delete=models.CASCADE, null=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name','last_name', 'is_active', 'is_staff', 'is_superuser']

#     object = UserManager()

#     class Meta(AbstractUser.Meta):
#         swappable = 'AUTH_USER_MODEL'

#     def __str__(self):
#         return self.email
