# from django.contrib.gis.db.models import PointField,PolygonField
from django.db import models
from django.core.validators import RegexValidator


class ZipCode(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    zip_code = models.CharField(max_length=5, null=False)
    state_id = models.CharField(null=False, max_length=2)
    state = models.CharField(null=False, max_length=100)
    borough = models.CharField(null=False, max_length=13)
    centroid_latitude = models.FloatField(null=False)
    centroid_longitude = models.FloatField(null=False)
    polygon = models.TextField(null=False)

    def __str__(self):
        return self.zip_code


class DropOffLocation(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=250)
    zip_code = models.ForeignKey(ZipCode, null=False, on_delete=models.CASCADE)
    # coordinates = PointField(srid=4326,null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    items_accepted = models.TextField(null=True)
    type = models.CharField(null=False, max_length=250)
    public_email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=17, null=True)
    street_address = models.TextField(null=False)

    def __str__(self):
        return str(self.id)
