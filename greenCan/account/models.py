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
