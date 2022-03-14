from django.shortcuts import render


def login(request):
    template = "account/templates/login.html"
    return render(request, template_name=template, context={})


def signup(request):
    template = "account/templates/signup.html"
    return render(request, template_name=template, context={})


def forget_password(request):
    template = "account/templates/forget-password.html"
    return render(request, template_name=template, context={})


def reset_password(request):
    template = "account/templates/reset-password.html"
    return render(request, template_name=template, context={})
