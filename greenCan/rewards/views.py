from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event, Image, Category, ImageMeta
from django.core.paginator import Paginator
import pyrebase
from recycle.models import ZipCode
from django.conf import settings
from django.contrib import messages
from uuid import uuid4
from django.utils.html import strip_tags
import sys


@login_required
@user_passes_test(lambda u: not u.is_staff)
def index(request):
    template_name = "rewards/templates/index.html"
    context = {}
    return render(request, template_name, context)


@login_required
def earn_rewards(request):
    if request.method == "POST":
        categories = request.POST.getlist("categories[]", None)
        event = request.POST.get("event", None)
        caption = request.POST.get("caption", None)
        location = request.POST.get("location", None)
        consent = request.POST.get("consent", False)
        images = request.FILES.getlist("file[]")

        firebase = pyrebase.initialize_app(settings.FIRE_BASE_CONFIG)
        auth = firebase.auth()
        auth_email = settings.FIREBASE_HOST_USER
        auth_pswd = settings.FIREBASE_HOST_PASSWORD
        firebase_user = auth.sign_in_with_email_and_password(auth_email, auth_pswd)
        storage = firebase.storage()
        urls = []

        if len(images) == 0:
            messages.error(request, "You need to upload at least one image to earn credits.")
            return redirect(reverse("rewards:earn-rewards"))

        if event is not None:
            event = Event.objects.filter(id=event)

        if event is None or len(event) == 0:
            messages.error(
                request,
                "You need to select an event, if none of the categories apply"
                ' in your case please select "Other".',
            )
            return redirect(reverse("rewards:earn-rewards"))

        user = request.user
        if location is not None and location != "":
            zip_code = ZipCode.objects.filter(zip_code=location)
            if len(zip_code) == 0:
                messages.error(
                    request,
                    "Please enter a valid 5 digit NYC zipcode."
                    " If it is not located in NYC please leave this field empty.",
                )
                return redirect(reverse("rewards:earn-rewards"))
            zip_code = zip_code[0]
        else:
            zip_code = None
        meta = None
        is_consent = consent == "consent"
        try:
            for image in images:
                if "test" not in sys.argv:
                    image_name = str(uuid4().int) + "." + image.name.split(".")[-1]
                else:
                    image_name = image.name
                storage.child("green-wall/" + image_name).put(image)
                url = storage.child("green-wall/" + image_name).get_url(firebase_user["idToken"])
                urls.append(url)

            if caption is not None:
                caption = strip_tags(caption)[:100]

            meta = ImageMeta(
                consent=is_consent,
                caption=caption,
                user=user,
                location=zip_code,
                event_type=event[0],
            )
            meta.save()

            if categories:
                for cat_id in categories:
                    cat_id = int(cat_id)
                    if Category.objects.get(pk=cat_id):
                        meta.category.add(cat_id)
                        meta.save()
            for url in urls:
                image = Image(image=url, meta=meta)
                image.save()
            messages.success(request, "Request submitted successfully.")
        except Exception:
            if meta is not None:
                meta.delete()
            messages.error(
                request,
                "Sorry, your request was not processed properly, please try again!",
            )
        return redirect(reverse("rewards:earn-rewards"))

    template_name = "rewards/templates/earn-rewards.html"
    events = Event.objects.all().order_by("name")
    categories = Category.objects.all().order_by("name")
    context = {"events": events, "categories": categories}
    return render(request, template_name, context)


def featured_image_gallery(request):
    if request.method == "POST":
        images = Image.objects.filter(meta__consent=True).order_by("-meta__uploaded_on", "-pk")
        images = Paginator(images, 20)
        page_number = request.POST.get("page", 1)
        if page_number == "":
            page_number = 1
        page = images.get_page(page_number)
        page_data = []
        for p in page:
            page_data.append(
                {
                    "image": p.image,
                    "description": p.meta.caption if p.meta.caption else "",
                    "event": p.meta.event_type.name,
                }
            )
        data = {
            "images": page_data,
        }
        if not page.has_next():
            data["has_next"] = 0
        else:
            data["next_page_number"] = page.next_page_number()
            data["has_next"] = 1
        return JsonResponse(data)

    template_name = "rewards/templates/featured-gallery.html"
    context = {}
    return render(request, template_name, context)
