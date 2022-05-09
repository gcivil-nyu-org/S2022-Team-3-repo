from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from reuse.models import Post
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class VolunteerLogs(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "id")
    reason = models.CharField(max_length=250, null=False, default="None")
    approved = models.CharField(default="False", max_length=10)
    approved_by = models.CharField(max_length=100, null=False, default="nyc.greencan@gmail.com")

    @property
    def is_approved(self):
        if self.content_object == Post:
            return str(self.approved)
        else:
            return str(self.approved)

    def __str__(self):
        return str(self.id)
