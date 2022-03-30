from django.test import TestCase, Client
from django.urls import reverse
from model_bakery import baker


class TestViews(TestCase):
    def setUp(self):
        self.index_url = reverse("recycle:index")
        self.url = reverse("recycle:fetch-drop-off-locations")
        self.zipcode = baker.make("recycle.ZipCode")
        self.dropoffloc = baker.make("recycle.DropOffLocation")
        self.client = Client()

    def test_index_GET(self):

        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "recycle/templates/index.html")

    # def test_searchdropofflocations1(self):

    #     print(self.zipcode.id)

    #     response = self.client.get(self.url + "?type=live-location&latitude=40.7362&longitude=-74.0422")

    #     self.assertEquals(response.status_code, 200)

    # def test_searchdropofflocations2(self):

    #     response = self.client.get(self.url + "?type=zipcode&zipcode=10004")

    #     self.assertEquals(response.status_code, 200)
