from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Event, Image, Category
from django.core.paginator import Paginator


@login_required
def index(request):
    template_name = "rewards/templates/index.html"
    events = Event.objects.all().order_by("name")
    categories = Category.objects.all().order_by("name")
    context = {"events": events, "categories": categories}
    return render(request, template_name, context)


@login_required
def earn_rewards(request):
    template_name = "rewards/templates/earn-rewards.html"
    context = {}
    return render(request, template_name, context)


def featured_image_gallery(request):
    template_name = "rewards/templates/featured-gallery.html"
    images = Image.objects.filter(consent=True).order_by("-uploaded_on")
    images = Paginator(images, 20)

    page_number = request.GET.get("page", 1)
    page = images.get_page(page_number)

    context = {"images": page}
    return render(request, template_name, context)
