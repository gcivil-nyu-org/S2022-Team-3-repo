import email
from django.db import models
from django.conf import settings
from notifications.base.models import AbstractNotification
from numpy import delete


# Create Notification Model
class Notification(AbstractNotification):

    def __str__(self):
        return str(self.id)
    
    class Meta(AbstractNotification.Meta):
        abstract = False
        
