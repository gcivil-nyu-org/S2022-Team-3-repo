from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from rewards.models import ImageMeta
from reuse.models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import VolunteerLogs
from django.contrib.sites.shortcuts import get_current_site
from notification.utils import create_notification
from accounts.utils import send_user_email, send_user_email_with_reasons


@login_required
@user_passes_test(lambda u: u.is_staff)
def index(request):
    template_name = "moderation/templates/index.html"
    posts = Post.objects.filter(approved=None).order_by("created_on")
    credit_requests = ImageMeta.objects.filter(approved=None).order_by("uploaded_on")
    context = {"posts": posts, "credit_request": credit_requests}
    return render(request, template_name=template_name, context=context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def review_post(request, id):
    id = int(id)
    template_name = "moderation/templates/review-post.html"
    if request.method == "POST":
        try:
            sender = request.user
            if "approve" in request.POST:
                id = request.POST["approve"]
                post = Post.objects.get(id=id)
                post.approved = True
                post.save()
                # send notification to user
                receiver = post.user
                msg_type = "approved"
                message = "Post approved successfully"
                notification = {
                    "sender": sender,
                    "receiver": receiver,
                    "msg_type": msg_type,
                    "message": message,
                }
                create_notification(notification)
                current_site = get_current_site(request)

                mail_subject = "Post " + str(post.title) + " approved"
                response = send_user_email(
                    receiver,
                    mail_subject,
                    receiver.email,
                    current_site,
                    "email/post-approval.html",
                    "email/post-approval-no-style.html",
                )
                messages.success(request, "Post Approved")
                return redirect("moderation:index")

            elif "deny" in request.POST:
                id = request.POST["deny"]
                post = Post.objects.get(id=id)
                post.approved = False
                post.save()
                reasons = []
                if "check1" in request.POST:
                    reasons.append(request.POST["check1"])
                if "check2" in request.POST:
                    reasons.append(request.POST["check2"])
                if "check3" in request.POST:
                    reasons.append(request.POST["check3"])
                if "description" in request.POST:
                    reasons.append(request.POST["description"])
                log = VolunteerLogs(post=post, reason=reasons, approved_by=sender)
                log.save()
                receiver = post.user
                msg_type = "denied"
                message = "; ".join(reasons)
                notification = {
                    "sender": sender,
                    "receiver": receiver,
                    "msg_type": msg_type,
                    "message": message,
                }
                create_notification(notification)
                current_site = get_current_site(request)

                mail_subject = "Post " + str(post.title) + " denied"
                response = send_user_email_with_reasons(
                    receiver,
                    mail_subject,
                    receiver.email,
                    current_site,
                    "email/post-denied.html",
                    "email/post-denied-no-style.html",
                    reasons,
                )
                if response != "success":
                    raise Exception("Failed to send email")
                messages.success(request, "Post Denied")
                return redirect("moderation:index")

        except Exception:
            messages.error(request, "Post approval Failed, contact admin")
        context = {}
        return render(request, template_name=template_name, context=context)

    post = get_object_or_404(Post, approved=None, pk=id)
    context = {"post": post}
    return render(request, template_name=template_name, context=context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def post_approval(request):

    return redirect("reuse:my-posts")
