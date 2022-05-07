from django.contrib import admin

# from .models import Post, Image, NGOLocation
from .models import Post, Image, NGOLocation, PostConcernLogs


class VolunteerAdmin(admin.AdminSite):
    site_header = "Volunteer Moderation page/"


class PostAdmin(admin.ModelAdmin):
    fields = ["title", "category", "approved"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


volunteer_site = VolunteerAdmin(name="VolunteerAdmin")
volunteer_site.register(Post, PostAdmin)
volunteer_site.register(Image)
volunteer_site.register(NGOLocation)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(NGOLocation)
admin.site.register(PostConcernLogs)
