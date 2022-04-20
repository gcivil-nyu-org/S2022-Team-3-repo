from django.shortcuts import render
from django.http import JsonResponse

from .models import Notification


"""
function: index

set path for notification page
"""


def index(request):
    template = "notification/templates/notification-index.html"
    context = {"is_notification": True}
    return render(request, template, context=context)


"""
function: get_notifications

get all notifications for a specific user ordered by the created time
so that the recent notification will be on the top of the list
"""


def get_notifications(request):
    if request.method == "POST":
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by("created_on")
    return JsonResponse(notifications)
