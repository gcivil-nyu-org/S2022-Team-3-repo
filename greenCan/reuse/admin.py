from django.contrib import admin

# from .models import Post, Image, NGOLocation
from .models import Post, Image, NGOLocation, PostConcernLogs
from accounts.models import VolunteerApplication


class VolunteerAdmin(admin.AdminSite):
    site_header = "Volunteer Moderation page/"

class VolunteerApplicationAdmin(admin.ModelAdmin):
    fields = ["score", "essay_1", "essay_2"]
    def has_view_permission(request):
        return True
    def has_change_permission(request,obj=None):
        return False
    # user = models.OneToOneField(
    #     User, on_delete=models.CASCADE, null=False, related_name="applicant"
    # )
    # submitted_on = models.DateTimeField(auto_now_add=True)
    # score = models.IntegerField(
    #     null=False, default=0, validators=[MaxValueValidator(5), MinValueValidator(0)]
    # )
    # essay_1 = models.TextField(max_length=500, null=False)
    # essay_2 = models.TextField(max_length=500, null=False)
    # approved_by = models.ForeignKey(
    #     User, null=False, on_delete=models.CASCADE, related_name="reviewer"
    # )
    # updated_on = models.DateTimeField(auto_now=True)


class PostAdmin(admin.ModelAdmin):
    fields = ["title", "category", "approved"]

    def has_add_permission(request):
        return False

    def has_delete_permission(request, obj=None):
        return False


volunteer_site = VolunteerAdmin(name="VolunteerAdmin")
volunteer_site.register(Post, PostAdmin)
volunteer_site.register(VolunteerApplication,VolunteerApplicationAdmin)
volunteer_site.register(Image)
volunteer_site.register(NGOLocation)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(NGOLocation)
admin.site.register(PostConcernLogs)
