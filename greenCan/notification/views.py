from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Notification


"""
function: index

set path for notification page
"""


@login_required
def index(request):
    template = "notification/templates/notification-index.html"
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by("-created_on")
    context = {"is_notification": True, "notifications": notifications}
    return render(request, template, context=context)


"""
function: get_notication

get all notifications of an input page number for a specific user
"""


@login_required
def get_notifications(request):
    user = request.user
    notificationObjects = Notification.objects.filter(user=user).order_by("-created_on")
    notificationObjects = Paginator(notificationObjects, 10)
    page_number = request.POST.get("page", 1)
    if page_number == "":
        page_number = 1
    page = notificationObjects.get_page(page_number)
    page_notifications = []

    for p in page:
        is_read = p.is_read
        created_on = p.created_on
        message_type = p.message_type
        messages = (p.message).split("; ")
        n = {
            "is_read": is_read,
            "created_on": created_on,
            "message_type": message_type,
            "messages": messages
        }
        page_notifications.append(n)
    
    result = {"notification": page_notifications}

    if not page.has_next():
        result["has_next"] = 0
    else:
        result["next_page_number"] = page.next_page_number()
        result["has_next"] = 1

    return JsonResponse(result)
