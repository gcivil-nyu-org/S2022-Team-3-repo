import pandas as pd
from geopy import distance
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core import serializers

def index(request):
    template = 'index.html'
    types = DropOffLocation.objects.values_list('type',flat=True).distinct()
    context = {
        'types': types
    }
    return render(request, template, context=context)


# user location is the location of the user i.e in form of latitude,longitude and if zipcode
# was entered by the user, then input shall be the centroid of the area
# response for all_locations should be something like :
# response = requests.get("https://data.cityofnewyork.us/resource/sxx4-xhzg.json")
# def min_dist_lat_long(search_result):
#     search_result = search_result
#     # check if user_location is a zip code or a tuple of latitude/longitude
#     # if zipcode

#     centroid_dict = search_result["centroid"]
#     site_dict = search_result["sites"]

#     my_location = (centroid_dict["latitude"], centroid_dict["longitude"])
    
#     # calculate distance for all locations
    
#     df = pd.DataFrame.from_dict(site_dict, orient='columns')
#     df["distance"] = 0
     
#     for i in range(len(df)):
#         try:
#             site_location = (df["latitude"].iloc[i],df["longitude"].iloc[i])
#             df["distance"].iloc[i] = distance.distance(my_location,site_location).km
#         except:
#             df["distance"].iloc[i] = float("inf")
#     df = df.sort_values(by=['distance'])
#     search_result = {"centroid": centroid_dict, 'sites': eval(df.to_json(orient='records'))}
#     return search_result

def get_dropoff_locations(centroid):
    logs_template = {
        'fields': [':local'],
    }
    sites_template = {
        'fields' : [':local',':related'],
        'related':{
            'logs': logs_template,
        }
    }
    locations = DropOffLocation.objects.raw(f'''
                SELECT F.ID AS ID,
                F.NAME AS NAME, 
                F.LATITUDE AS LATITUDE, 
                F.LONGITUDE AS LONGITUDE, 
                F.TYPE AS TYPE,
                COALESCE(F.ITEMS_ACCEPTED,'') AS ITEMS_ACCEPTED, 
                COALESCE(F.PUBLIC_EMAIL,'') AS EMAIL, 
                COALESCE(F.PHONE_NUMBER,'') AS PUBLIC_PHONE,
                F.ZIP_CODE_ID AS ZIP_CODE_ID FROM 
                    (
                        SELECT *,row_number() over (partition by TYPE order by D.DISTANCE desc) as TYPE_RANK FROM 
                        (
                        SELECT *,calculate_distance(40.627038489795, -74.02457508163266, R.LATITUDE, R.LONGITUDE, 'M') AS DISTANCE
                            FROM RECYCLE_DROPOFFLOCATION AS R
                            ORDER BY DISTANCE
                        ) AS D
                    ) AS F
                WHERE F.TYPE_RANK<11''').prefetch_related('zip_code')
    sites = []
    for location in locations:
        name = location.name
        zip_code = location.zip_code.zip_code
        state_id = location.zip_code.state_id
        latitude = location.latitude
        longitude = location.longitude
        items_accepted = location.items_accepted if location.items_accepted else ''
        category = location.type
        email = location.public_email if location.public_email else ''
        phone_number = location.phone_number if location.phone_number else ''
        street_address = location.street_address
        site = {'name': name, 'zip_code': zip_code, 'state_id': state_id, 'latitude': latitude,
                'longitude': longitude, 'item_accepted': items_accepted, 'type': category,
                'email': email, 'phone_number': phone_number, 'street_address': street_address}
        sites.append(site)
    # sites = serializers.serialize('json',locations,**sites_template)
    # print(sites)
    # print("=="*100)
    # print(sites[0])
    return sites

@csrf_exempt
def search_dropoff_locations(request):
    if request.GET.get('type')=='zipcode':
        zipcode = request.GET.get('zipcode')
        zip_location = ZipCode.objects.filter(zip_code=zipcode).first()
        if zip_location ==  None:
            err_flag = True
            err_msg = "Please enter a valid NYC zip code"
            return JsonResponse({'err_flag': err_flag, 'err_msg': err_msg})
        else:
            centroid = {'latitude': zip_location.centroid_latitude, 'longitude': zip_location.centroid_longitude}
    elif request.GET.get('type')=='live-location':
        user_lat = request.GET.get('latitude')
        user_long = request.GET.get('longitude')
        centroid = {'latitude': user_lat, 'longitude': user_long}
    else:
        err_msg = "Invalid arguments provided"
        return JsonResponse({'err_flag': err_flag, 'err_msg': err_msg})
    sites = get_dropoff_locations(centroid)
    search_result = {"centroid": centroid, 'sites': sites}
    search_result['err_flag'] = False
    return JsonResponse(search_result)
    
# @csrf_exempt
# def search_locations_by_zipcode(request):
#     zipcode = request.GET.get('zipcode')
#     zip_location = ZipCode.objects.filter(zip_code=zipcode).first()
#     if zip_location ==  None:
#         err_flag = True
#         err_msg = "Please enter a valid NYC zip code"
#         return JsonResponse({'err_flag': err_flag, 'err_msg': err_msg})
#     else:
#         centroid = {'latitude': zip_location.centroid_latitude, 'longitude': zip_location.centroid_longitude}
#         sites = get_dropoff_locations(centroid)
#         search_result = {"centroid": centroid, 'sites': sites}
#         search_result['err_flag'] = False
#         return JsonResponse(search_result)


# @csrf_exempt
# def search_locations_by_current_location(request):
#     user_lat = request.GET.get('latitude')
#     user_long = request.GET.get('longitude')
#     centroid = {'latitude': user_lat, 'longitude': user_long}
#     sites = get_dropoff_locations(centroid)
#     search_result = {"centroid": centroid, 'sites': sites}
#     search_result['err_flag'] = False
#     return JsonResponse(search_result)
