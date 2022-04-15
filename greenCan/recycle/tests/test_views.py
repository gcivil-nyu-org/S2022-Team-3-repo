from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker
from django.utils.encoding import force_str

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
        """
        test to check if index page is returning a valid response
        """

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "recycle/templates/index.html")

    def test_search_dropoff_locations1(self):
        """
        test to check if searching by user's current location is returning a valid response
        """

        response = self.client.get(
            self.url + "?type=live-location&latitude=40.7362&longitude=-74.0422"
        )

        self.assertEquals(response.status_code, 200)

    def test_search_dropoff_locations2(self):
        """
        test to check if searching by zip code is returning a valid response
        """

        response = self.client.get(self.url + "?type=zipcode&zipcode=10001")

        self.assertEquals(response.status_code, 200)

    def test_search_dropoff_locations_invalid_zip_code(self):
        """
        test to check if searching by an invalid zip code is returning a correct error message
        """

        response = self.client.get(self.url + "?type=zipcode&zipcode=10004")

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            force_str(response.content),
            {"err_flag": True, "err_msg": "Please enter a valid NYC zip code"},
        )

    def test_dropoff_locations_invalid_data(self):
        """
        test to check if searching by unknown type is returning a correct error message
        """

        response = self.client.get(self.url + "?type=somerandomstring")

        self.assertEquals(response.status_code, 200)
        self.assertJSONEqual(
            force_str(response.content),
            {"err_flag": True, "err_msg": "Invalid arguments provided"},
        )
