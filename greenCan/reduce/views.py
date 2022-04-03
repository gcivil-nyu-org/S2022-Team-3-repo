from django.shortcuts import render


"""
function: index

set path for reuse page
"""


def index(request):
    template = "reduce/templates/reduce-index.html"
    context = {"is_reduce": True}
    return render(request, template, context=context)
