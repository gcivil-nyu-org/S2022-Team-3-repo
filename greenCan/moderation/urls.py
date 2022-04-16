from django.urls import path

from . import views

app_name = "moderation"

urlpatterns = [
    path("", views.index, name="index"),
    path("review/post/<int:id>", views.review_post, name="review-post"),
    # path("review/credit-request/<int:id>", views.review_credit_request, name="review-post"),
]
