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


class PostConcernLogsAdmin(admin.ModelAdmin):
    list_display = ('post', 'created_on')
    change_form_template = 'reuse/templates/admin/change_form.html'

    def change_view(self, request, object_id, extra_context=None):
        post_concern = PostConcernLogs.objects.get(pk=object_id)
        moderated = False

        if request.POST:
            admin_form = self.get_form(request, post_concern)(request.POST)

            if admin_form.is_valid():
                message = admin_form.cleaned_data['message']
                if 'approve' in request.POST:
                    moderated = True
                    post_concern.approve(request.user, message)
                    post_concern.checked = True
                    post_concern.message = message
                    post_concern.save()
                elif 'reject' in request.POST:
                    moderated = True
                    post_concern.reject(request.user, message)
                    post_concern.checked = True
                    post_concern.message = message
                    post_concern.save()
                

        extra_context = {
            'post_url': 'greencan.heroku.com/post/' + str(post_concern.post.id),
            'moderated': moderated,
        }
        return super().change_view(request, object_id, extra_context=extra_context)


volunteer_site = VolunteerAdmin(name="VolunteerAdmin")
volunteer_site.register(Post, PostAdmin)
volunteer_site.register(Image)
volunteer_site.register(NGOLocation)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(NGOLocation)
admin.site.register(PostConcernLogs, PostConcernLogsAdmin)
