from django.contrib import admin

# Register your models here.
from .models import Post, Image

admin.site.register(Post)
admin.site.register(Image)
