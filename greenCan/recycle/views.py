from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import *

def index(request):
    template = 'index.html'
    return render(request, template, context={})


def search_locations_by_zipcode(request):
    zipcode = request.GET.get('zipcode')
    err_flag = False
    err_msg = ''
    zip_locations = ZipCode.objects.filter(zip_code=zipcode)
    if zip_locations.count() == 0:
        err_flag = True
        err_msg = "Please enter a valid NYC zip code"
        return JsonResponse({'err_flag': err_flag, 'err_msg': err_msg})
    else:
        centroid = {'latitude': zip_locations[0].centroid_latitude, 'longitude': zip_locations[0].centroid_longitude}
        # print(centroid)
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
        json_data = json.dumps(search_result)
        # print(json_data)
        # print(type(json_data))


def search_locations_by_current_location(request):
    user_lat = request.GET.get('latitude')
    user_long = request.GET.get('longitude')
    centroid = {'latitude': user_lat, 'longitude': user_long}
    print(centroid)
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
    json_data = json.dumps(search_result)
    print(json_data)

