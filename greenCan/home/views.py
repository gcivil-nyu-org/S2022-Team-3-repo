from django.shortcuts import render


def index(request):
    template = "home/templates/index.html"
    return render(request, template, context={})
