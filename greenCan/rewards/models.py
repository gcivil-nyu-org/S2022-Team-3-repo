from django.db import models
from django.conf import settings
from recycle.models import ZipCode
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class CreditsLookUp(models.Model):
    action = models.CharField(primary_key=True, max_length=200)
    credit = models.PositiveIntegerField(null=True, default=None)


class EarnGreenCredits(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    action = models.ForeignKey(CreditsLookUp, on_delete=models.CASCADE)
    earned_on = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


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
    green_credits = GenericRelation(EarnGreenCredits)


class Image(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    meta = models.ForeignKey(ImageMeta, on_delete=models.CASCADE)
    image = models.URLField(max_length=2000, null=False, unique=True)
