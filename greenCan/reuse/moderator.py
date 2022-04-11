from moderation import moderation
from moderation.moderator import GenericModerator

from .models import Post,Image


# class AnotherModelModerator(GenericModerator):
    # Add your moderator settings for AnotherModel here

moderation.register(Post)  # Uses default moderation settings
moderation.register(Image)
# moderation.register(AnotherModel, AnotherModelModerator)  # Uses custom moderation settings