from django.contrib import admin

# from .models import Post, Image, NGOLocation
from .models import Post, Image, NGOLocation, PostConcernLogs
from accounts.models import VolunteerApplication,User
from notification.utils import create_notification

# class ReadOnlyAdminMixin:
#     def has_add_permission(self, request):
#         if not request.user.is_superuser:
#             return False

#     def has_change_permission(self, request, obj=None):

#         if not request.user.is_superuser:
#             return False

#     def has_delete_permission(self, request, obj=None):
#         if not request.user.is_superuser:
#             return False

#     def has_view_permission(self, request, obj=None):
#         if not request.user.is_superuser:
#             return False    

class VolunteerAdmin(admin.AdminSite):
    site_header = "Volunteer Moderation page/"

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ("score","essay_1","essay_2","approved")
    def get_form(self, request, obj=None,**kwargs):
        form  = super().get_form(request,obj,**kwargs)
        form.base_fields['user'].disabled = True
        form.base_fields['approved_by'].disabled = True

        
        return form

    def save_model(self, request, obj, form, change):
        #convert object to dict values
        cleaned_data = form.cleaned_data
        user = cleaned_data.get('user')
        user = User.objects.get(email="pb2640@nyu.edu")
        approved = cleaned_data.get('approved')
        if(approved):
            print(user.is_staff)
            user.staff = True
            user.save()
        else:
            user.staff = False
            user.save()

        
        

        #approving form after clicking save
        # if(form["approved"]==True):
        #     #change the applicants status from user to staff
        #     #first get user
        #     user = form["user"]
        #     user.is_staff = True
        #     user.save()
        #     # send the notification
        #     #TODO


        #     #send the email
        #     #TODO

        

        # if(form.fields["approved"]==True):
        #     print("Yes")
        # else:
        #     print("NO")
        # notification = {
        #             "sender": sender,
        #             "receiver": receiver,
        #             "msg_type": msg_type,
        #             "message": message,
        #             "notification_obj": post,
        #         }
        # create_notification(notification)
        return super().save_model(request, obj, form, change)


    


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
