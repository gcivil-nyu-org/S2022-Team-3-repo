from django.shortcuts import render


ERROR_PAGE_TEMPLATE = "helper/templates/error-page-template.html"


def error_400(request, *args, **argv):
    context = {
        "title": "Bad Request",
        "code": 400,
        "errortitle": "OPPS! Something Went Wrong.",
        "errortext": "Your reqeust was not processed.",
    }
    response = render(
        request,
        template_name=ERROR_PAGE_TEMPLATE,
        context=context,
        status=context["code"],
    )
    return response


def error_403(request, *args, **argv):
    context = {
        "title": "Permission Denied",
        "code": 403,
        "errortitle": "UH OH! You're lost.",
        "errortext": "You cannot access this page.",
    }
    response = render(
        request,
        template_name=ERROR_PAGE_TEMPLATE,
        context=context,
        status=context["code"],
    )
    return response


def error_404(request, *args, **argv):
    context = {
        "title": "Page Not Found",
        "code": 404,
        "errortitle": "UH OH! You're lost.",
        "errortext": "The page you are looking for does not exist.",
    }
    response = render(
        request,
        template_name=ERROR_PAGE_TEMPLATE,
        context=context,
        status=context["code"],
    )
    return response


def error_405(request, *args, **argv):
    context = {
        "title": "Method Not Allowed",
        "code": 405,
        "errortitle": "UH OH! You're lost.",
        "errortext": "",
    }
    response = render(
        request,
        template_name=ERROR_PAGE_TEMPLATE,
        context=context,
        status=context["code"],
    )
    return response


def error_500(request, *args, **argv):
    context = {
        "title": "Internal Server Error",
        "code": 500,
        "errortitle": "OPPS! Something Went Wrong",
        "errortext": "",
    }
    response = render(
        request,
        template_name=ERROR_PAGE_TEMPLATE,
        context=context,
        status=context["code"],
    )
    return response


def error_502(request, *args, **argv):
    context = {
        "title": "Bad Gateway",
        "code": 502,
        "errortitle": "UH OH! You're lost.",
        "errortext": "",
    }
    response = render(
        request,
        template_name=ERROR_PAGE_TEMPLATE,
        context=context,
        status=context["code"],
    )
    return response
