from django.shortcuts import render

def index(request):
    template = 'index.html'
    return render(request, template, context={})


def search_locations_by_zipcode(request):
    zipcode = request.GET.get('zipcode')
    print(zipcode)