from django.db import models
from django.conf import settings
from recycle.models import ZipCode


class Category(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True)


class Event(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, null=False, unique=True)


class ImageMeta(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    category = models.ManyToManyField(Category)
    event_type = models.ForeignKey(Event, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    location = models.ForeignKey(ZipCode, null=True, on_delete=models.CASCADE)
    caption = models.CharField(max_length=150, null=True)
    consent = models.BooleanField(default=False)
    approved = models.BooleanField(null=True, default=None)
    uploaded_on = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    meta = models.ForeignKey(ImageMeta, on_delete=models.CASCADE)
    image = models.URLField(max_length=2000, null=False, unique=True)
