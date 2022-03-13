from django.shortcuts import render


"""
function: index

set path for homepage
"""


def index(request):
    template = "home/templates/index.html"
    return render(request, template, context={})
