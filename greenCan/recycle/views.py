from django.shortcuts import render

def index(request):
    template = 'index.html'
    return render(request, template, context={})