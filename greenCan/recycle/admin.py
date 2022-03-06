from django.contrib import admin

from .models import DropOffLocation, ZipCode

admin.site.register(ZipCode)
admin.site.register(DropOffLocation)
