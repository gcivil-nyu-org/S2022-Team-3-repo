from datetime import datetime
from django.shortcuts import render, redirect
from .models import Post, Image
from recycle.models import ZipCode
import pyrebase
from account.models import Account


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
    template = "listingPage.html"
    posts = Post.objects.all().values()
    images = Image.objects.all().values()
    zip_codes = ZipCode.objects.all().values()
    for index in range(len(posts)):
        posts[index]["url"] = images.filter(post=posts[index]["id"])[0]["url"]
        temp = zip_codes.filter(id=posts[index]["zip_code_id"])[0]
        posts[index]["location"] = str(
            temp["borough"] + ", " + temp["state"] + ", " + temp["zip_code"]
        )

    context = {"Posts": posts, "is_reuse": True}
    return render(request, template, context=context)


"""
function: create_post

Firstly, set configuration for Google firebase cloud storage
then obtain post data and images from frontend
save the images to firebase and get urls
create Post object and Images object for this user's post and save into database
"""


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
    auth_email = "nyc.greencan@gmail.com"
    auth_pswd = "Tandon123"
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

    user = Account.objects.filter(first_name="John")
    zip_code = ZipCode.objects.filter(zip_code=zipcode)

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
            user=user[0],
            created_on=datetime.now(),
        )
        post.save()

        for url in urls:
            image = Image(url=url, post=post)
            image.save()

    return redirect("/reuse/donations")
