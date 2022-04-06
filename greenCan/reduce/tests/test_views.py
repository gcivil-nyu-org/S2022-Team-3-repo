from django.test import TestCase, Client
from django.urls import reverse

from recycle.models import ZipCode
from reduce.models import RetailerLocation


class TestViews(TestCase):
    def setUp(self):
        self.index_url = reverse("reduce:index")
        self.url = reverse("reduce:fetch-retailer-locations")
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
        retailer_location = RetailerLocation(
            name="Target",
            zip_code=zipcode,
            latitude=40.75021293296376,
            longitude=-73.99692994900218,
            type="Paper Bag",
            phone="2121112011",
            address="101 Willoughby street",
        )
        retailer_location.save()
        self.retailer_location = retailer_location

    def test_index_GET(self):
        """
        test to check if index page is returning a valid response
        """

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "reduce/templates/reduce-index.html")

    def test_retailer_locations1(self):
        """
        test to check if searching by zip code is returning a valid response
        """

        response = self.client.get(
            self.url + "?type=live-location&latitude=40.7362&longitude=-74.0422"
        )

        self.assertEquals(response.status_code, 200)

    def test_retailer_locations2(self):
        """
        test to check if searching by zip code is returning a valid response
        """

        response = self.client.get(self.url + "?type=zipcode&zipcode=10001")

        self.assertEquals(response.status_code, 200)
