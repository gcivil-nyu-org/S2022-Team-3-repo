from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    template_name = "rewards/templates/index.html"
    context = {}
    return render(request, template_name, context)


@login_required
def earn_rewards(request):
    template_name = "rewards/templates/earn-rewards.html"
    context = {}
    return render(request, template_name, context)
