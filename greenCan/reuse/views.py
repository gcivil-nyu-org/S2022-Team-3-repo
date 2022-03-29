from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Post, Image, NGOLocation
from recycle.models import ZipCode
import pyrebase
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings


"""
function: index

set path for reuse page
"""


def index(request):
    template = "reuse_index.html"
    context = {"is_reuse": True}
    return render(request, template, context=context)


"""
function: donation_view

set path for donation view page
"""


def donation_view(request):
    template = "reuse/templates/donate-item-page.html"
    context = {"is_reuse": True}
    return render(request, template, context=context)


"""
function: listing_page

Obtain all posts in database with their images
then rebuild the data format for frontend view
"""


def listing_page(request):
    template = "listing-page.html"
    posts = Post.objects.all()
    context = {"posts": posts, "is_reuse": True}
    return render(request, template, context=context)


"""
function: create_post

Firstly, set configuration for Google firebase cloud storage
then obtain post data and images from frontend
save the images to firebase and get urls
create Post object and Images object for this user's post and save into database
"""


@login_required
def create_post(request):
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
        storage.child(image.name).put(image)
        url = storage.child(image.name).get_url(user["idToken"])
        urls.append(url)

    title = request.POST.get("title")
    description = request.POST.get("description")
    category = request.POST.get("category")
    number = request.POST.get("number")
    email = request.POST.get("email")
    zipcode = request.POST.get("zipcode")
    user = request.user
    zip_code = ZipCode.objects.filter(zip_code=zipcode)

    if len(zip_code) == 0:
        zip_code = None

    if (
        title is not None
        and description is not None
        and category is not None
        and number is not None
        and email is not None
        and zip_code is not None
    ):
        post = Post(
            title=title,
            category=category,
            phone_number=number,
            email=email,
            zip_code=zip_code[0],
            description=description,
            user=user,
        )
        post.save()

        for url in urls:
            image = Image(url=url, post=post)
            image.save()

    return redirect(reverse("reuse:donation-page"))


"""
function: ngo_donation

Set path for ngo donation page
"""


def ngo_donation(request):
    template = "reuse/templates/ngo-donation.html"
    context = {"is_reuse": True}
    return render(request, template, context=context)


"""
function: get_ngo_locations

Query all NGO drop-off locations from database
Then reformat each drop-off location data for frontend
"""


def get_ngo_locations(centroid):
    locations = NGOLocation.objects.raw(
        f"""
            SELECT F.ID AS ID,
            F.LATITUDE AS LATITUDE,
            F.LONGITUDE AS LONGITUDE,
            COALESCE(F.ITEMS_ACCEPTED,'') AS ITEMS_ACCEPTED,
            COALESCE(F.EMAIL,'') AS EMAIL,
            COALESCE(F.PHONE,'') AS PHONE,
            COALESCE(F.HOURS,'') AS HOURS,
            COALESCE(F.WEBSITE,'') AS WEBSITE
            FROM
                (
                    SELECT *,
                    row_number() over (order by D.DISTANCE asc) as TYPE_RANK
                    FROM
                    (
                    SELECT *,
                        calculate_distance({centroid['latitude']}, {centroid['longitude']}, R.LATITUDE, R.LONGITUDE, 'M') AS DISTANCE
                        FROM REUSE_NGOLOCATION AS R
                    ) AS D
                ) AS F
            WHERE F.TYPE_RANK<40
            ORDER BY F.DISTANCE;"""
    ).prefetch_related("zip_code")

    sites = []
    for location in locations:
        zip_code = location.zip_code.zip_code
        state_id = location.zip_code.state_id
        borough = location.zip_code.borough
        latitude = location.latitude
        longitude = location.longitude
        items_accepted = location.items_accepted if location.items_accepted else ""
        email = location.email if location.email else ""
        phone_number = location.phone if location.phone else ""
        street_address = location.address
        hours = location.hours if location.hours else ""
        website = location.website if location.website else ""
        site = {
            "zip_code": zip_code,
            "state_id": state_id,
            "latitude": latitude,
            "longitude": longitude,
            "item_accepted": items_accepted,
            "email": email,
            "phone_number": phone_number,
            "street_address": street_address,
            "hours": hours.replace(
                ", ", ', <i class="fa fa-clock"></i> <span class="text-black">'
            )
            .replace(",", ",</span>")
            .replace(",", "<br>"),
            "website": website,
            "borough": borough,
        }
        sites.append(site)
    return sites


"""
function: search_ngo_locations

take user's input zip code from frontend
then validate this zip code
if it is valid, then sort all NGO drop-off locations in database
by the distance from centroid of the zip code to the NGO drop-off location
otherwise, return an error message
"""


@csrf_exempt
def search_ngo_locations(request):
    if request.GET.get("type") == "zipcode":
        zipcode = request.GET.get("zipcode")
        zip_location = ZipCode.objects.filter(zip_code=zipcode).first()
        if zip_location is None:
            err_flag = True
            err_msg = "Please enter a valid NYC zip code"
            return JsonResponse({"err_flag": err_flag, "err_msg": err_msg})
        else:
            centroid = {
                "latitude": zip_location.centroid_latitude,
                "longitude": zip_location.centroid_longitude,
            }
    elif request.GET.get("type") == "live-location":
        user_lat = request.GET.get("latitude")
        user_long = request.GET.get("longitude")
        centroid = {"latitude": user_lat, "longitude": user_long}
    else:
        err_msg = "Invalid arguments provided"
        err_flag = True
        return JsonResponse({"err_flag": err_flag, "err_msg": err_msg})
    sites = get_ngo_locations(centroid)
    search_result = {"centroid": centroid, "sites": sites}
    search_result["err_flag"] = False
    return JsonResponse(search_result)
