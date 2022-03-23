from django.test import TestCase, Client
from django.urls import reverse
from recycle.models import ZipCode, DropOffLocation
from model_bakery import baker
import json
import sqlite3
import math
from django.conf import settings
from django.db import connection

class TestViews(TestCase):

    def setUp(self):
        self.index_url = reverse('recycle:index')
        self.url = reverse('recycle:fetch-drop-off-locations')
        self.zipcode = baker.make('recycle.ZipCode')
        self.dropoffloc = baker.make('recycle.DropOffLocation')

        

        # define user defined function
        def calc_distance(lat1, lon1, lat2, lon2, unit):
            if ((lat1 == lat2) and (lon1 == lon2)):
                return 0
            else:
                radlat1 = math.pi * lat1/180
                radlat2 = math.pi * lat2/180
                theta = lon1-lon2
                radtheta = math.pi * theta/180
                dist = math.sin(radlat1) * math.sin(radlat2) + math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta)
                if (dist > 1):
                    dist = 1
                dist = math.acos(dist)
                dist = dist * 180/math.pi
                dist = dist * 60 * 1.1515
                if unit=="K":
                    dist = dist * 1.609344
                if unit=="N": 
                    dist = dist * 0.8684
                return dist

        
        
        # create the user defined function
        connection.connection.create_function("calculate_distance", 5, calc_distance)



        self.client = Client()

    def test_index_GET(self):
                
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recycle/templates/index.html')
"""
    def test_searchdropofflocations1(self):

        print(self.zipcode.id)
        
        response = self.client.get(self.url + "?type=live-location&latitude=40.7362&longitude=-74.0422")

        self.assertEquals(response.status_code, 200)

    def test_searchdropofflocations2(self):       
             

        response = self.client.get(self.url + "?type=zipcode&zipcode=10004")

        self.assertEquals(response.status_code, 200)

"""

    

        
        



        


       

        

        



   
