from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import RetailerLocation
from recycle.models import ZipCode

"""
function: index

set path for reuse page
"""


def index(request):
    template = "reduce/templates/reduce-index.html"
    context = {"is_reduce": True}
    return render(request, template, context=context)


"""
function: get_retailer_locations

Query all eco-friendly goods store locations from database
Then reformat each store location data for frontend
"""


def get_retailer_locations(centroid):
    locations = RetailerLocation.objects.raw(
        f"""
            SELECT F.ID AS ID,
            F.NAME AS NAME,
            F.LATITUDE AS LATITUDE,
            F.LONGITUDE AS LONGITUDE,
            F.TYPE AS TYPE,
            COALESCE(F.PHONE,'') AS PHONE
            FROM
                (
                    SELECT *,
                    row_number() over (order by D.DISTANCE asc) as TYPE_RANK
                    FROM
                    (
                    SELECT *,
                        calculate_distance(
                            {centroid['latitude']},
                            {centroid['longitude']},
                            R.LATITUDE, R.LONGITUDE, 'M'
                        ) AS DISTANCE
                        FROM REDUCE_RETAILERLOCATION AS R
                    ) AS D
                ) AS F
            WHERE F.TYPE_RANK<25
            ORDER BY F.DISTANCE;"""
    ).prefetch_related("zip_code")

    sites = []
    for location in locations:
        zip_code = location.zip_code.zip_code
        state_id = location.zip_code.state_id
        borough = location.zip_code.borough
        latitude = location.latitude
        longitude = location.longitude
        name = location.name
        phone_number = location.phone if location.phone else ""
        street_address = location.address
        category = location.type
        site = {
            "zip_code": zip_code,
            "state_id": state_id,
            "latitude": latitude,
            "longitude": longitude,
            "name": name,
            "phone_number": phone_number,
            "street_address": street_address,
            "borough": borough,
            "type": category,
        }
        sites.append(site)
    return sites


"""
function: search_retailer_locations

take user's input zip code from frontend, then validate this zip code
if it is valid, then sort all retailer locations in database
by the distance from centroid of the zip code to the retailer location
otherwise, return an error message
"""


@csrf_exempt
def search_retailer_locations(request):
    if request.GET.get("type") == "zipcode":
        zipcode = request.GET.get("zipcode")
        zip_location = ZipCode.objects.filter(zip_code=zipcode).first()
        if zip_location is None:
            err_flag = True
            err_msg = "Please enter a valid NYC zip code"
            return JsonResponse({"err_flag": err_flag, "err_msg": err_msg})
        else:
            centroid = {
                "latitude": zip_location.centroid_latitude,
                "longitude": zip_location.centroid_longitude,
            }
    elif request.GET.get("type") == "live-location":
        user_lat = request.GET.get("latitude")
        user_long = request.GET.get("longitude")
        centroid = {"latitude": user_lat, "longitude": user_long}
    else:
        err_flag = True
        err_msg = "Invalid arguments provided"
        return JsonResponse({"err_flag": err_flag, "err_msg": err_msg})
    sites = get_retailer_locations(centroid)
    search_result = {"centroid": centroid, "sites": sites}
    search_result["err_flag"] = False
    return JsonResponse(search_result)
