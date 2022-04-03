from django.db import models
from recycle.models import ZipCode


class RetailerLocation(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    zip_code = models.ForeignKey(ZipCode, null=False, on_delete=models.CASCADE)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    phone = models.CharField(max_length=17, null=True)
    name = models.CharField(max_length=250)
    address = models.TextField(null=False)
    type = models.CharField(null=False, max_length=250)

    def __str__(self):
        return str(self.id)
