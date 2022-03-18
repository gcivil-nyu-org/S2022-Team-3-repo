from django.shortcuts import render


def index(request):
    template_name = "home/templates/index.html"
    context = {}
    return render(request, template_name=template_name, context=context)
