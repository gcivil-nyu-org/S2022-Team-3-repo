from django.shortcuts import render


"""
function: index

set path for homepage
"""


def index(request):
    template_name = "home/templates/index.html"
    context = {}
    return render(request, template_name=template_name, context=context)
