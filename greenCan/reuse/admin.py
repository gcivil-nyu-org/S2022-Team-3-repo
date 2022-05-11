from django.contrib import admin
from accounts.utils import send_user_email

# from .models import Post, Image, NGOLocation
from .models import Post, Image, NGOLocation, PostConcernLogs
from accounts.models import VolunteerApplication, User
from notification.utils import create_notification
from django.contrib.sites.shortcuts import get_current_site


class VolunteerAdmin(admin.AdminSite):
    site_header = "Volunteer Moderation page/"


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ("score", "essay_1", "essay_2", "approved")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        # convert object to dict values
        cleaned_data = form.cleaned_data
        user = cleaned_data.get("user")
        sender = cleaned_data.get("approved_by")
        user = User.objects.get(email=user)
        approved = cleaned_data.get("approved")
        if approved:
            user.staff = True
            user.save()
            msg_type = "success"
            message = "Volunteer Application Approved"

            notification = {
                "sender": sender,
                "receiver": user,
                "msg_type": msg_type,
                "message": message,
                "notification_obj": None,
            }
            create_notification(notification)
            current_site = get_current_site(request)
            mail_subject = "Congratulations, you're a volunteer"
            response = send_user_email(
                user,
                mail_subject,
                user.email,
                current_site,
                "email/volunteer-approval.html",
                "email/volunteer-approval-no-style.html",
            )
            if response != "success":
                raise Exception("Failed to send email")
        else:
            user.staff = False
            user.save()
            msg_type = "error"
            message = "Volunteer Application Denied"

            notification = {
                "sender": sender,
                "receiver": user,
                "msg_type": msg_type,
                "message": message,
                "notification_obj": None,
            }
            create_notification(notification)
            current_site = get_current_site(request)
            mail_subject = "We have an update on your volunteer Application"
            response = send_user_email(
                user,
                mail_subject,
                user.email,
                current_site,
                "email/volunteer-denied.html",
                "email/post-denied-no-style.html",
            )
            if response != "success":
                raise Exception("Failed to send email")

        return super().save_model(request, obj, form, change)


class PostAdmin(admin.ModelAdmin):
    fields = ["title", "category", "approved"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.site.register()
class PostConcernLogsAdmin(admin.ModelAdmin):
    readonly_fields = ("checked",)
    list_display = ("post", "created_on", "checked")
    change_form_template = "reuse/templates/admin/change_form.html"

    def change_view(self, request, object_id, extra_context=None):
        post_concern = PostConcernLogs.objects.get(pk=object_id)

        if request.POST:
            admin_form = self.get_form(request, post_concern)(request.POST)

            if admin_form.is_valid():
                message = admin_form.cleaned_data["message"]
                current_site = get_current_site(request)
                if "approve" in request.POST:
                    post_concern.send_signals_and_moderate(request.user, 1, current_site, message)
                elif "reject" in request.POST:
                    post_concern.send_signals_and_moderate(request.user, 0, current_site, message)

        extra_context = {
            "post_url": "/reuse/post-details/?postID=" + str(post_concern.post.id),
            "moderated": post_concern.checked,
            "is_post_concern_log": True,
        }
        return super().change_view(request, object_id, extra_context=extra_context)


volunteer_site = VolunteerAdmin(name="VolunteerAdmin")
volunteer_site.register(Post, PostAdmin)
volunteer_site.register(VolunteerApplication, VolunteerApplicationAdmin)
volunteer_site.register(Image)
volunteer_site.register(NGOLocation)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(NGOLocation)
admin.site.register(PostConcernLogs, PostConcernLogsAdmin)
