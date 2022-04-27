from django.db import models

# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey
from reuse.models import Post
from django.contrib.contenttypes.models import ContentType

class VolunteerLogs(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #add a content_type here
    content_object = GenericForeignKey('content_type','id')
    reason = models.CharField(max_length=250, null=False, default="None")
    approved = models.CharField(default="False", max_length=10)
    approved_by = models.CharField(max_length=100, null=False, default="nyc.greencan@gmail.com")
    # user_email = models.EmailField(null=True) #email of users post

    @property
    def is_approved(self):
        print("approved working")
        if(self.content_object==Post):
            return str(self.approved)
        else:
            return str(self.approved)

    # @property
    # def user_email(self):
    #     if(self.content_object==Post):
    #         return self.content_object.email
    #     else:
    #         return str(self.content_object.user.email)

    def __str__(self):
        return str(self.id)

