from notifications.base.models import AbstractNotification


# Create Notification Model
class Notification(AbstractNotification):
    def __str__(self):
        return str(self.id)

    class Meta(AbstractNotification.Meta):
        abstract = False
