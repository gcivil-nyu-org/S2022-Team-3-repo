from django.db import models
from greenCan.account.models import Account
from greenCan.recycle.models import ZipCode


class Post(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=250, null=False)
    category = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=17, null=True)
    email = models.EmailField(null=True)
    zip_code = models.ForeignKey(ZipCode, null=False, on_delete=models.CASCADE)
    description = models.TextField(null=False)
    user = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True, default=False)
    still_available = models.BooleanField(null=True, default=True)

    def __str__(self):
        return str(self.id)


class Image(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    url = models.URLField(max_length=500, null=False)

    def __str__(self):
        return str(self.id)
