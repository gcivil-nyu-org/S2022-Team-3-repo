from django.db import models
from django.conf import settings

# Create Notification Model


class Notification(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    message = models.TextField(null=False)
    is_read = models.BooleanField(default=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(null=False, max_length=20)

    def __str__(self):
        return str(self.id)
