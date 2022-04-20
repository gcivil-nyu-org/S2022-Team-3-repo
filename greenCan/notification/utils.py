from notifications.signals import notify
from .models import Notification


def create_notification(notification):
    sender = notification.get("sender")
    receiver = notification.get("receiver")
    message = notification.get("message")
    msg_type = notification.get("msg_type")

    notification = Notification(
        user=receiver,
        message=message,
        message_type=msg_type,
    )
    notification.save()

    notify.send(sender, recipient=receiver, verb="Notification", description=message)
