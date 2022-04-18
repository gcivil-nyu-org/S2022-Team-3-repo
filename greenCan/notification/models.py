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

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """
    This Notification consumer handles websocket connections for clients.
    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async.
    """
    # WebSocket event handlers

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        try:
            # Pass auth token as a part of url.
            token = self.scope.get('url_route', {}).get(
                'kwargs', {}).get('token', False)
            logger = logging.getLogger(__name__)
            # If no token specified, close the connection
            if not token:
                logger.error('No token supplied')
                await self.close()
            # Try to authenticate the token from DRF's Token model
            try:
                token = Token.objects.select_related('user').get(key=token)
            except Token.DoesNotExist:
                logger.error("Token doesn't exist")
                await self.close()

            if not token.user.is_active:
                logger.error('User not active')
                await self.close()
            user = token.user

            # Get the group to which user is to be subscribed.
            group_name = user.group_name

            # Add this channel to the group.
            await self.channel_layer.group_add(
                group_name,
                self.channel_name,
            )
            await self.accept()
        except Exception as e:
            logger.error(e)
            await self.close()

    async def disconnect(self, code):
        """
        Called when the websocket closes for any reason.
        Leave all the rooms we are still in.
        """
        try:
            # Get auth token from url.
            token = self.scope.get('url_route', {}).get(
                'kwargs', {}).get('token', False)
            logger = logging.getLogger(__name__)
            try:
                token = Token.objects.select_related('user').get(key=token)
            except Token.DoesNotExist:
                logger.error(
                    "Token doesn't exist while closing the connection")
            user = token.user

            # Get the group from which user is to be kicked.
            group_name = user.group_name

            # kick this channel from the group.
            await self.channel_layer.group_discard(group_name, self.channel_name)
        except Exception as e:
            logger.error(e)