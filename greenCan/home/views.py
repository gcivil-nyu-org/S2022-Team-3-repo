from django.shortcuts import render
from rewards.models import EarnGreenCredits
from django.db.models import Sum, Window,F
from django.db.models.functions import Rank
from django.db.models.functions.window import RowNumber
from accounts.models import User

"""
function: index

set path for homepage
"""


def index(request):
    template_name = "home/templates/index.html"
    result = EarnGreenCredits.objects.values('user').annotate(totalCredits=Sum('action__credit')).annotate(rank=Window(expression=Rank(), order_by=F('totalCredits').desc()))
    #postNum = EarnGreenCredits.objects.filter(user=request.user, action="post").count()
    if request.user:
        print("I am NOT none")
    else:
        print("I am none")
    try:
        gold = result[0]
        user1 = User.objects.get(pk=gold["user"])
    except IndexError:
        gold = 'null'
        user1 = 'null'
    
    try:
        silver = result[1]
        user2 = User.objects.get(pk=silver["user"])
    except IndexError:
        silver = 'null'
        user2 = 'null'
    
    try:
        bronze = result[2]
        user3 = User.objects.get(pk=bronze["user"])
    except IndexError:
        bronze = 'null'
        user3 = 'null'
    
    #print(result)
    context = {
        "gold": gold,
        "silver": silver,
        "bronze": bronze,
        "user1": user1,
        "user2": user2,
        "user3": user3,
        "user": request.user,
        #"post_num": postNum
    }
    return render(request, template_name=template_name, context=context)
