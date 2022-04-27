# import imp
from django.contrib import admin

from .models import Category, Image, Event, ImageMeta, CreditsLookUp, EarnGreenCredits


admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Image)
admin.site.register(ImageMeta)
admin.site.register(CreditsLookUp)
admin.site.register(EarnGreenCredits)
