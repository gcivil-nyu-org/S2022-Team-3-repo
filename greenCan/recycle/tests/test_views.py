from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker

from recycle.models import ZipCode, DropOffLocation


class TestViews(TestCase):
    def setUp(self):
        self.index_url = reverse("recycle:index")
        self.url = reverse("recycle:fetch-drop-off-locations")
        self.dropoffloc = baker.make("recycle.DropOffLocation")
        self.client = Client()
        zipcode = ZipCode(
            zip_code="10001",
            state_id="NY",
            state="New York",
            borough="Manhattan",
            centroid_latitude=40.75021293296376,
            centroid_longitude=-73.99692994900218,
            polygon="",
        )
        zipcode.save()
        self.zipcode = zipcode
        drop_off_location = DropOffLocation(
            name="Drop-Off-1",
            zip_code=zipcode,
            latitude=40.75021293296376,
            longitude=-73.99692994900218,
            items_accepted="Food",
            type="public recycle",
            public_email="tandon@nyu.edu",
            phone_number="2121112011",
            street_address="101 Willoughby street",
        )
        drop_off_location.save()
        self.drop_off_location = drop_off_location

    def test_index_GET(self):

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "recycle/templates/index.html")

    def test_searchdropofflocations1(self):

        response = self.client.get(
            self.url + "?type=live-location&latitude=40.7362&longitude=-74.0422"
        )

        self.assertEquals(response.status_code, 200)

    def test_searchdropofflocations2(self):

        response = self.client.get(self.url + "?type=zipcode&zipcode=10004")

        self.assertEquals(response.status_code, 200)
