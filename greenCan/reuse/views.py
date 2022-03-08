from re import template
from django.shortcuts import render
from .models import Post,Image
from recycle.models import ZipCode

def index(request):
    template = 'reuse_index.html'
    return render(request, template, context={})

def donation_view(request):
    template = "donate-item-page.html"
    context = {"is_reuse": True}
    return render(request, template, context=context)


def listingPage(request):
    template = 'listingPage.html'
    Posts = Post.objects.all().values()
    Images = Image.objects.all().values()
    ZipCodes = ZipCode.objects.all().values()
    for index in range(len(Posts)):
        # add the url
        Posts[index]["url"] = Images.filter(post_id = Posts[index]["id"])[0]["url"]
        temp = ZipCodes.filter(id = Posts[index]["zip_code_id"])[0]
        Posts[index]["location"] = str(temp["borough"]+", "+temp["state"]+", "+temp["zip_code"])
        

    context = {"Posts":Posts,"is_reuse": True}
    return render(request,template,context = context)