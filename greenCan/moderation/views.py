from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from rewards.models import ImageMeta
from reuse.models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages


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
            if "approve" in request.POST:
                id = request.POST["approve"]
                post = Post.objects.get(id=id)
                post.approved = True
                post.save()
                messages.success(request, "Post Approved")
            elif "deny" in request.POST:
                id = request.POST["deny"]
                post = Post.objects.get(id=id)
                post.approved = False
                post.save()
                messages.success(request, "Post Denied")

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
