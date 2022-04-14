from django.contrib import admin

# from .models import Post, Image, NGOLocation
from . import models

class VolunteerAdmin(admin.AdminSite):
    site_header = "Volunteer Moderation page/"

volunteer_site = VolunteerAdmin(name="VolunteerAdmin")
volunteer_site.register(models.Post)
volunteer_site.register(models.Image)
volunteer_site.register(models.NGOLocation)
# admin.site.register(Post)
# admin.site.register(Image)
# admin.site.register(NGOLocation)
