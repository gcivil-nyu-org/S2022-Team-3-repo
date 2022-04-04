# import imp
from django.contrib import admin

from .models import Category, Image, Event, ImageMeta


admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Image)
admin.site.register(ImageMeta)
