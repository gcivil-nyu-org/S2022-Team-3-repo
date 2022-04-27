from notifications.signals import notify
from rewards.models import ImageMeta


def create_notification(notification):
    sender = notification.get("sender")
    receiver = notification.get("receiver")
    notification_obj = notification.get("notification_obj")
    verb_str = "post"
    if type(notification_obj) == ImageMeta:
        verb_str = "imagemeta"

    message_type = notification.get("msg_type")
    message = notification.get("message")

    notify.send(
        sender=sender,
        recipient=receiver,
        verb=verb_str,
        level=message_type,
        action_object=notification_obj,
        description=message,
    )
