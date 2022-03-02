import pandas as pd
from geopy import distance
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *


def index(request):
    template = 'index.html'
    return render(request, template, context={})


# user location is the location of the user i.e in form of latitude,longitude and if zipcode
# was entered by the user, then input shall be the centroid of the area
# response for all_locations should be something like :
# response = requests.get("https://data.cityofnewyork.us/resource/sxx4-xhzg.json")
def min_dist_lat_long(search_result):
    search_result = search_result
    # # check if user_location is a zip code or a tuple of latitude/longitude
    # # if zipcode
    centroid_dict = search_result["centroid"]
    site_dict = search_result["sites"]

    my_location = (centroid_dict["latitude"], centroid_dict["longitude"])
    # # try:
    # #     if(type(user_location)==int):
    # #         zip = int(user_location)
    # #         for it in models.ZipCode.objects.filter(zip_code=zip).values():
    # #             my_location = (it["centroid_latitude"],it["centroid_longitude"])
    # #     elif(type(user_location)==tuple):
    # #         latitude,longitude = user_location[0],user_location[1]
    # #         my_location = (latitude,longitude)
    # # except:
    # #     return {"Location could not be found"}


    # # calculate distance for all locations
    
    df = pd.DataFrame.from_dict(site_dict, orient='columns')
    df["distance"] = 0
     
    for i in range(len(df)):
        try:
            site_location = (df["latitude"].iloc[i],df["longitude"].iloc[i])
            df["distance"].iloc[i] = distance.distance(my_location,site_location).km
        except:
            df["distance"].iloc[i] = float("inf")
            # dont display inf in sorted list
    df = df.sort_values(by=['distance'])
    # locations = df
    # sites = []
    # for i in range(len(locations)):
    #     name = locations["name"][i]
    #     zip_code = locations["zip_code"][i].
    #     state_id = locations[i].zip_code.state_id
    #     latitude = locations[i].latitude
    #     longitude = locations[i].longitude
    #     items_accepted = locations[i].items_accepted
    #     category = locations[i].type
    #     email = locations[i].public_email
    #     phone_number = locations[i].phone_number
    #     street_address = locations[i].street_address
    #     site = {'name': name, 'zip_code': zip_code, 'state_id': state_id, 'latitude': latitude,
    #             'longitude': longitude, 'item_accepted': items_accepted, 'type': category,
    #             'email': email, 'phone_number': phone_number, 'street_address': street_address}
    #     sites.append(site)
    search_result = {"centroid": centroid_dict, 'sites': eval(df.to_json(orient='records'))}
    return search_result


@csrf_exempt
def search_locations_by_zipcode(request):
    zipcode = request.GET.get('zipcode')
    zip_locations = ZipCode.objects.filter(zip_code=zipcode)
    if zip_locations.count() == 0:
        err_flag = True
        err_msg = "Please enter a valid NYC zip code"
        return JsonResponse({'err_flag': err_flag, 'err_msg': err_msg})
    else:
        centroid = {'latitude': zip_locations[0].centroid_latitude, 'longitude': zip_locations[0].centroid_longitude}
        locations = DropOffLocation.objects.all()
        sites = []
        for i in range(locations.count()):
            name = locations[i].name
            zip_code = locations[i].zip_code.zip_code
            state_id = locations[i].zip_code.state_id
            latitude = locations[i].latitude
            longitude = locations[i].longitude
            items_accepted = locations[i].items_accepted
            category = locations[i].type
            email = locations[i].public_email
            phone_number = locations[i].phone_number
            street_address = locations[i].street_address
            site = {'name': name, 'zip_code': zip_code, 'state_id': state_id, 'latitude': latitude,
                    'longitude': longitude, 'item_accepted': items_accepted, 'type': category,
                    'email': email, 'phone_number': phone_number, 'street_address': street_address}
            sites.append(site)

        search_result = {"centroid": centroid, 'sites': sites}
        sorted_json_data = min_dist_lat_long(search_result)
        sorted_json_data['err_flag'] = False
        return JsonResponse(sorted_json_data)


@csrf_exempt
def search_locations_by_current_location(request):
    user_lat = request.GET.get('latitude')
    user_long = request.GET.get('longitude')
    centroid = {'latitude': user_lat, 'longitude': user_long}
    locations = DropOffLocation.objects.all()
    sites = []
    for i in range(locations.count()):
        name = locations[i].name
        zip_code = locations[i].zip_code.zip_code
        state_id = locations[i].zip_code.state_id
        latitude = locations[i].latitude
        longitude = locations[i].longitude
        items_accepted = locations[i].items_accepted
        category = locations[i].type
        email = locations[i].public_email
        phone_number = locations[i].phone_number
        street_address = locations[i].street_address
        site = {'name': name, 'zip_code': zip_code, 'state_id': state_id, 'latitude': latitude,
                'longitude': longitude, 'item_accepted': items_accepted, 'type': category,
                'email': email, 'phone_number': phone_number, 'street_address': street_address}
        sites.append(site)

    search_result = {"centroid": centroid, 'sites': sites}
    sorted_json_data = min_dist_lat_long(search_result)
    sorted_json_data['err_flag'] = False
    return JsonResponse(sorted_json_data)


