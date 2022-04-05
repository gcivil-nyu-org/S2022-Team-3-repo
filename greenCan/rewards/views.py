from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Event, Image, Category, ImageMeta
from django.core.paginator import Paginator
import pyrebase
from recycle.models import ZipCode
from django.conf import settings
from django.contrib import messages


@login_required
def index(request):
    template_name = "rewards/templates/index.html"
    context = {}
    return render(request, template_name, context)


@login_required
def earn_rewards(request):

    if request.method == "POST":
        categories = request.POST.get("categories[]", None)
        event = request.POST.get("event", None)
        caption = request.POST.get("caption")
        location = request.POST.get("location", None)
        consent = request.POST.get("consent", False)
        images = request.FILES.getlist("file[]")
        config = {
            "apiKey": "AIzaSyDTyK0Z4z6YPG_gx7Ue8bS7Nasv747a5-8",
            "authDomain": "greencan-tandon.firebaseapp.com",
            "projectId": "greencan-tandon",
            "databaseURL": "https://greencan-tandon-default-rtdb.firebaseio.com/",
            "storageBucket": "greencan-tandon.appspot.com",
            "messagingSenderId": "957653486728",
            "appId": "1:957653486728:web:ddb27d2cf6067972c6e33d",
        }

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        auth_email = settings.FIREBASE_HOST_USER
        auth_pswd = settings.FIREBASE_HOST_PASSWORD
        user = auth.sign_in_with_email_and_password(auth_email, auth_pswd)
        storage = firebase.storage()
        urls = []
        for image in images:
            storage.child("green-wall/" + image.name).put(image)
            url = storage.child("green-wall/" + image.name).get_url(user["idToken"])
            urls.append(url)
        user = request.user
        if location is not None:
            zip_code = ZipCode.objects.filter(zip_code=location)

        if location is None or len(zip_code) == 0:
            zip_code = None
        meta = None
        is_consent = consent is not False
        try:
            meta = ImageMeta(
                consent=is_consent,
                caption=caption,
                user=user,
                event_type=Event.objects.get(pk=event),
            )
            meta.save()
            print(dir(meta))
            for category in categories:
                meta.category.add(category)

            meta.save()

            for url in urls:
                image = Image(image=url, meta=meta)
                image.save()
            messages.success(request, "Request processed successfully.")
            return redirect(reverse("rewards:earn-rewards"))
        except Exception as e:
            print(e)
            if meta is not None:
                meta.delete()
            messages.error(request, "Failed!")
            return redirect(reverse("rewards:earn-rewards"))

    template_name = "rewards/templates/earn-rewards.html"
    events = Event.objects.all().order_by("name")
    categories = Category.objects.all().order_by("name")
    context = {"events": events, "categories": categories}
    return render(request, template_name, context)


def featured_image_gallery(request):
    template_name = "rewards/templates/featured-gallery.html"
    images = Image.objects.filter(meta__consent=True).order_by("-uploaded_on")
    images = Paginator(images, 20)
    page_number = request.GET.get("page", 1)
    if page_number == "":
        page_number = 1

    page = images.get_page(page_number)
    context = {"images": page}
    if not page.has_next():
        context["show_banner"] = True
        context["next_page"] = False
    else:
        context["next_page"] = page.next_page_number()
    if page_number == 1:
        context["first"] = True
    return render(request, template_name, context)
