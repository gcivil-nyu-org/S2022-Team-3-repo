from django.shortcuts import render
from rewards.models import EarnGreenCredits, Image
from django.db.models import Sum, Window, F
from django.db.models.functions import Rank

from accounts.models import User

"""
function: index

set path for homepage
"""


def index(request):
    template_name = "home/templates/index.html"
    result = (
        EarnGreenCredits.objects.values("user")
        .annotate(totalCredits=Sum("action__credit"))
        .annotate(rank=Window(expression=Rank(), order_by=F("totalCredits").desc()))
    )
    # postNum = EarnGreenCredits.objects.filter(user=request.user, action="post").count()
    try:
        gold = result[0]
        user1 = User.objects.get(pk=gold["user"])
    except IndexError:
        gold = None
        user1 = None

    try:
        silver = result[1]
        user2 = User.objects.get(pk=silver["user"])
    except IndexError:
        silver = None
        user2 = None

    try:
        bronze = result[2]
        user3 = User.objects.get(pk=bronze["user"])
    except IndexError:
        bronze = None
        user3 = None

    if request.user.is_authenticated:
        postNum = EarnGreenCredits.objects.filter(user=request.user, action="post").count()
        metaNum = EarnGreenCredits.objects.filter(user=request.user, action="image").count()
        earned_credits = EarnGreenCredits.objects.filter(user=request.user).aggregate(
            Sum("action__credit")
        )
        userImageMeta = EarnGreenCredits.objects.filter(
            user=request.user, action="image"
        ).values_list("object_id", flat=True)
        # print(userImageMeta)
        ImgNum = Image.objects.filter(meta__pk__in=userImageMeta).count()

        if postNum + metaNum == 0:
            rank = None
        else:
            rank = (
                EarnGreenCredits.objects.values("user")
                .annotate(totalCredits=Sum("action__credit"))
                .filter(totalCredits__gt=earned_credits["action__credit__sum"])
                .count()
                + 1
            )
        context = {
            "gold": gold,
            "silver": silver,
            "bronze": bronze,
            "user1": user1,
            "user2": user2,
            "user3": user3,
            "user": request.user,
            "post_num": postNum,
            "image_meta_num": metaNum,
            "image_num": ImgNum,
            "rank": rank,
        }
    else:
        context = {
            "gold": gold,
            "silver": silver,
            "bronze": bronze,
            "user1": user1,
            "user2": user2,
            "user3": user3,
            "user": request.user,
        }
    return render(request, template_name=template_name, context=context)
