from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)


class Images(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)


class Post(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=250)
    category = models.TextField(null=True)
    phone_number = models.CharField(max_length=17, null=True)
    email = models.EmailField(null=True)
    zip_code = models.CharField(max_length=5, null=False)
    description = models.TextField(null=False)
    images = models.ForeignKey(Images, null=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True)
    still_available = models.BooleanField(null=True)
