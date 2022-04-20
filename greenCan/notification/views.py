from django.shortcuts import render


"""
function: index

set path for notification page
"""


def index(request):
    template = "notification/templates/notification-index.html"
    context = {"is_notification": True}
    return render(request, template, context=context)
