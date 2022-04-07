from django.shortcuts import render


def error400(request):
    context = {
        'title': 'Bad Request',
        'code': 400,
        'errortitle': 'OPPS! Something went wrong.',
        'errortext': 'Your reqeust was not processed.'
    }
    return render(request, 'helper/templates/error-page-template.html', context)

def error404(request):
    context = {
        'title': 'Page Not Found',
        'code': 404,
        'errortitle': 'UH OH! You\'re lost.',
        'errortext': 'The page you are looking for does not exist.'
    }
    return render(request, 'helper/templates/error-page-template.html', context)

def error500(request):
    context = {
        'title': 'Page Not Found',
        'code': 400,
        'errortitle': '',
        'errortext': ''
    }
    return render(request, 'helper/templates/error-page-template.html', context)

def error505(request):
    context = {
        'title': 'Page Not Found',
        'code': 400,
        'errortitle': '',
        'errortext': ''
    }
    return render(request, 'helper/templates/error-page-template.html', context)
