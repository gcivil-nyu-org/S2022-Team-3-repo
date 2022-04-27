from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from rewards.models import ImageMeta, EarnGreenCredits, CreditsLookUp
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
    template_name = "moderation/templates/review-post.html"
    if request.method == "POST":
        try:
            reasons = []
            sender = request.user
            if "approve" in request.POST:

                id = request.POST["approve"]
                post = Post.objects.get(id=int(id))
                post.approved = True
                post.save()

                # add credit to approved post
                EarnGreenCredits.objects.create(
                    object_id=post.id,
                    content_object=post,
                    action=CreditsLookUp.objects.get(action="post"),
                    user=post.user,
                )

                log = VolunteerLogs(content_object=post, reason=reasons, approved_by=sender.email)
                log.save()
                # send notification to user
                receiver = post.user
                msg_type = "success"
                message = "Post approved successfully"
                notification = {
                    "sender": sender,
                    "receiver": receiver,
                    "msg_type": msg_type,
                    "message": message,
                    "notification_obj": post,
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
                if response != "success":
                    raise Exception("Failed to send email")
                messages.success(request, "Post Approved")
                return redirect("moderation:index")

            elif "deny" in request.POST:
                id = request.POST["deny"]
                post = Post.objects.get(id=int(id))
                post.approved = False
                post.save()
                if "check1" in request.POST:
                    reasons.append(request.POST["check1"])
                if "check2" in request.POST:
                    reasons.append(request.POST["check2"])
                if "check3" in request.POST:
                    reasons.append(request.POST["check3"])
                if "description" in request.POST:
                    reasons.append(request.POST["description"])
                log = VolunteerLogs(content_object=post, reason=reasons, approved_by=sender.email)
                log.save()
                receiver = post.user
                msg_type = "error"
                message = "; ".join(reasons)
                notification = {
                    "sender": sender,
                    "receiver": receiver,
                    "msg_type": msg_type,
                    "message": message,
                    "notification_obj": post,
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
def review_credit_request(request, id):
    id = int(id)
    template_name = "moderation/templates/review-credit.html"
    if request.method == "POST":
        try:
            reasons = []
            sender = request.user
            if "approve" in request.POST:
                id = request.POST["approve"]
                img_meta = ImageMeta.objects.get(id=int(id))
                img_meta.approved = True
                img_meta.save()

                EarnGreenCredits.objects.create(
                    object_id=img_meta.id,
                    content_object=img_meta,
                    action=CreditsLookUp.objects.get(action="image"),
                    user=img_meta.user,
                )

                log = VolunteerLogs(
                    content_object=img_meta, reason=reasons, approved_by=sender.email
                )
                log.save()
                # send notification to user
                receiver = img_meta.user
                msg_type = "success"
                message = "Credit request approved successfully"
                notification = {
                    "sender": sender,
                    "receiver": receiver,
                    "msg_type": msg_type,
                    "message": message,
                    "notification_obj": img_meta,
                }
                create_notification(notification)
                current_site = get_current_site(request)

                mail_subject = "Post " + str(img_meta.caption) + " approved"
                response = send_user_email(
                    receiver,
                    mail_subject,
                    receiver.email,
                    current_site,
                    "email/post-approval.html",
                    "email/post-approval-no-style.html",
                )
                messages.success(request, "Credit request Approved")
                return redirect("moderation:index")

            elif "deny" in request.POST:
                id = request.POST["deny"]
                img_meta = ImageMeta.objects.get(id=int(id))
                img_meta.approved = False
                img_meta.save()
                reasons = []
                if "check1" in request.POST:
                    reasons.append(request.POST["check1"])
                if "check2" in request.POST:
                    reasons.append(request.POST["check2"])
                if "check3" in request.POST:
                    reasons.append(request.POST["check3"])
                if "description" in request.POST:
                    reasons.append(request.POST["description"])
                log = VolunteerLogs(
                    content_object=img_meta, reason=reasons, approved_by=sender.email
                )
                log.save()
                receiver = img_meta.user
                msg_type = "error"
                message = "; ".join(reasons)
                notification = {
                    "sender": sender,
                    "receiver": receiver,
                    "msg_type": msg_type,
                    "message": message,
                    "notification_obj": img_meta,
                }
                create_notification(notification)
                current_site = get_current_site(request)

                mail_subject = "Post " + str(img_meta.caption) + " denied"
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

        except Exception as e:
            print(e)
            messages.error(request, "Post approval Failed, contact admin")
        context = {}
        return render(request, template_name=template_name, context=context)

    img_meta = get_object_or_404(ImageMeta, approved=None, pk=id)
    categories = img_meta.category.all()
    context = {"img_meta": img_meta, "categories": categories}
    return render(request, template_name=template_name, context=context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def post_approval(request):
    return redirect("reuse:my-posts")
