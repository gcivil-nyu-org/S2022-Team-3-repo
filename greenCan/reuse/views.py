from django.shortcuts import render

# Create your views here.
def listingPage(request):
    return render(request,'listingPage.html')
