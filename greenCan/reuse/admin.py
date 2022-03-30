from django.contrib import admin

from .models import Post, Image, NGOLocation

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(NGOLocation)
