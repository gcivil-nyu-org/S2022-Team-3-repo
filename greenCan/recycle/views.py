from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DropOffLocation, ZipCode


def index(request):
    template = "recycle/templates/index.html"
    types = DropOffLocation.objects.values_list("type", flat=True).distinct()
    context = {"types": types}
    return render(request, template, context=context)


def get_dropoff_locations(centroid):
    locations = DropOffLocation.objects.raw(
        f"""
            SELECT F.ID AS ID,
            F.NAME AS NAME,
            F.LATITUDE AS LATITUDE,
            F.LONGITUDE AS LONGITUDE,
            F.TYPE AS TYPE,
            COALESCE(F.ITEMS_ACCEPTED,'') AS ITEMS_ACCEPTED,
            COALESCE(F.PUBLIC_EMAIL,'') AS EMAIL,
            COALESCE(F.PHONE_NUMBER,'') AS PUBLIC_PHONE
            FROM
                (
                    SELECT *,
                    row_number() over (partition by TYPE order by D.DISTANCE asc) as TYPE_RANK
                    FROM
                    (
                    SELECT *,
                        calculate_distance({centroid['latitude']}, {centroid['longitude']}, R.LATITUDE, R.LONGITUDE, 'M') AS DISTANCE
                        FROM RECYCLE_DROPOFFLOCATION AS R
                    ) AS D
                ) AS F
            WHERE F.TYPE_RANK<11
            ORDER BY F.DISTANCE;"""
    ).prefetch_related("zip_code")
    sites = []
    for location in locations:
        name = location.name
        zip_code = location.zip_code.zip_code
        state_id = location.zip_code.state_id
        latitude = location.latitude
        longitude = location.longitude
        items_accepted = location.items_accepted if location.items_accepted else ""
        category = location.type
        email = location.public_email if location.public_email else ""
        phone_number = location.phone_number if location.phone_number else ""
        street_address = location.street_address
        site = {
            "name": name,
            "zip_code": zip_code,
            "state_id": state_id,
            "latitude": latitude,
            "longitude": longitude,
            "item_accepted": items_accepted,
            "type": category,
            "email": email,
            "phone_number": phone_number,
            "street_address": street_address,
        }
        sites.append(site)
    return sites


@csrf_exempt
def search_dropoff_locations(request):
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
        err_msg = "Invalid arguments provided"
        return JsonResponse({"err_flag": err_flag, "err_msg": err_msg})
    sites = get_dropoff_locations(centroid)
    search_result = {"centroid": centroid, "sites": sites}
    search_result["err_flag"] = False
    return JsonResponse(search_result)
