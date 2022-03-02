
from django.shortcuts import render
import requests
import pandas as pd
from geopy import distance
from . import models
from django.shortcuts import render
from django.http import JsonResponse
import json
# from models import ZipCode

def index(request):
    template = 'index.html'
    return render(request, template, context={})


#user location is the location of the user i.e in form of latitude,longitude and if zipcode 
# was entered by the user, then input shall be the centroid of the area
# response for all_locations should be something like : response = requests.get("https://data.cityofnewyork.us/resource/sxx4-xhzg.json")
def min_dist_lat_long(search_result):
    #check if user_location is a zip code or a tuple of latitude/longitude
    #if zipcode
    centroid_dict = search_result["centroid"]
    site_dict = search_result["sites"]

    my_location = (centroid_dict["latitude"],centroid_dict["longitude"])
    # try:
    #     if(type(user_location)==int):
    #         zip = int(user_location)
    #         for it in models.ZipCode.objects.filter(zip_code=zip).values():
    #             my_location = (it["centroid_latitude"],it["centroid_longitude"])
    #     elif(type(user_location)==tuple):
    #         latitude,longitude = user_location[0],user_location[1]
    #         my_location = (latitude,longitude)
    # except:
    #     return {"Location could not be found"}
        

    #calculate distance for all locations
    
    df = pd.DataFrame.from_dict(site_dict, orient='columns')
    df["distance"] = 0
     
    for i in range(len(df)):
        try:
            site_location = (df["latitude"].iloc[i],df["longitude"].iloc[i])
            df["distance"].iloc[i] = distance.distance(my_location,site_location).km
        except:
            df["distance"].iloc[i] = float("inf")
            #dont display inf in sorted list 
    df = df.sort_values(by=['distance'])
    return df.to_json()




    
