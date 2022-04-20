from django.db import models

# Create your models here.

from reuse.models import Post


class VolunteerLogs(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    reason = models.CharField(max_length=250, null=False, default="None")

    @property
    def is_approved(self):
        return self.post.approved

    def __str__(self):
        return str(self.id)
