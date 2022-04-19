from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from rewards.models import ImageMeta
from reuse.models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


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
    post = get_object_or_404(Post, approved=None, pk=id)
    context = {"post": post}
    return render(request, template_name=template_name, context=context)
