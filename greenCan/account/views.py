from django.shortcuts import render


def login(request):
    if request.method == "GET":
        template = "account/templates/login.html"
        return render(request, template_name=template, context={})


def signup(request):
    if request.method == "GET":
        template = "account/templates/signup.html"
        return render(request, template_name=template, context={})


def forget_password(request):
    if request.method == "GET":
        template = "account/templates/forget-password.html"
        return render(request, template_name=template, context={})


def reset_password(request):
    if request.method == "GET":
        template = "account/templates/reset-password.html"
        return render(request, template_name=template, context={})
