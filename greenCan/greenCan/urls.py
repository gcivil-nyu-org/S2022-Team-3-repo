"""greenCan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from accounts import views
from reuse.admin import volunteer_site

admin.site.site_header = "GreenCan Admin/Volunteer Panel"
admin.site.site_title = "GreenCan Admin/Volunteer Panel"
admin.site.index_title = "GreenCan Admin/Volunteer Panel"

urlpatterns = [
    path("", include("home.urls")),
    path("admin/", admin.site.urls, name="admin"),
    path("volunteers/", volunteer_site.urls),
    path("recycle/", include("recycle.urls")),
    path("reuse/", include("reuse.urls")),
    path("reduce/", include("reduce.urls")),
    path("accounts/", include("accounts.urls")),
    path("social/social/signup/", views.account_exists, name="socialaccount_signup"),
    path("rewards/", include("rewards.urls")),
    path("social/", include("allauth.urls"), name="social"),
    path("notification/", include("notification.urls")),
    path("volunteer/", include("moderation.urls")),
    re_path("^inbox/notifications/", include("notifications.urls", namespace="notifications")),
]

handler400 = "helper.views.error_400"

handler403 = "helper.views.error_403"

handler404 = "helper.views.error_404"

handler405 = "helper.views.error_405"

handler500 = "helper.views.error_500"

handler502 = "helper.views.error_502"
