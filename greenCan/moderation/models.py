from django.db import models

# Create your models here.

from reuse.models import Post


class VolunteerLogs(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    reason = models.CharField(max_length=250, null=False, default="None")
    approved = models.CharField(default="False", max_length=10)
    approved_by = models.CharField(max_length=100, null=False, default="nyc.greencan@gmail.com")
    user_email = models.EmailField(null=True)

    @property
    def is_approved(self):
        return str(self.post.approved)

    @property
    def user_email(self):
        return self.post.email

    def __str__(self):
        return str(self.id)
