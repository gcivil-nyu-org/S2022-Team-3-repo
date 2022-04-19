from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages


def send_notification(request):
    try:
        if request.method == 'POST':
            sender = User.objects.get(username=request.user)
            receiver = User.objects.get(id=request.POST.get('user_id'))
            notify.send(sender, recipient=receiver, verb='Notification', description=request.POST.get('message'))
            return redirect('index')
        else:
            return HttpResponse("Invalid request")
    except Exception as e:
        print(e)
        return HttpResponse("Please login from admin site for sending messages")


def create_notificaiton(request):
    if(
        message is not None
        and msg_type is not None
    ):

        user = request.user
        message = request.POST.get("message")
        msg_type = request.POST.get("msg_type")

        notification = Notification(
            user=user,
            message=message,
            message_type=msg_type,
        )
        notification.save()

        messages.success(request, "Notification created successfully")
    else:
        messages.error(
            request,
            "Failed to create the notificaiton. Please make sure you"
            + " fill in all fields",
        )
