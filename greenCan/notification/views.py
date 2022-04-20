from django.shortcuts import render

from .models import Notification


"""
function: index

set path for notification page
"""


def index(request):
    template = "notification/templates/notification-index.html"
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by("-created_on")
    context = {"is_notification": True, "notifications": notifications}
    return render(request, template, context=context)
