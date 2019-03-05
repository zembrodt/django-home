from django.shortcuts import redirect, render
from django.conf import settings
from django.http.response import JsonResponse
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    UpdateView,
)
from pyowm.exceptions.api_call_error import APICallTimeoutError
from pyowm.exceptions.api_response_error import NotFoundError
from urllib.request import urlopen
from urllib.parse import quote
from datetime import datetime, timedelta
from dashboard.models import Module
from dashboard.forms import (
    WeatherForm
)
from .models import Weather
import json, math, pyowm, os

owm = pyowm.OWM(settings.OWM_KEY)

# NOTE: placeholder
def weather(request, module):
    #weather = Weather.objects.get(module=module)
    template = get_template('weather/weather.html')
    context = {
        'id': module.id
    }
    return template.render(context)

def update_weather_stats(request):
    if request.method == 'GET':
        module_id = request.GET.get('id')
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')

        print(f'latitude: {latitude}\nlongitude: {longitude}')

        city = 'London'
        country = 'UK'
        observation = None
        if latitude is None or longitude is None:
            # Default location
            observation = owm.weather_at_place('London,UK')
        else:
            utc_now = datetime.utcnow()

            city, country = get_location(latitude, longitude)
            utc_offset = get_timezone(latitude, longitude)
            
            now = utc_now + timedelta(hours=utc_offset)

            time_of_day = 'day' if now.hour >= 7 and now.hour < 20 else 'night'

            print(f'current time: {now}')
            print(f'current utc time: {utc_now}')
            print(f'utc offset: {utc_offset}')
            #observation = owm.weather_at_coords(latitude, longitude)

            # TODO: get list of cities OWM has for calculated city,country
            # Find the coords of each city and choose the one with the closest distance

            # Get all observations matching the city
            observations = None
            tries = 0
            #while observations is None or tries < 5:
            #    try:
            #        tries += 1
                    # TODO: speed this up?
                    #observations = owm.weather_at_places(f'{city},{country}', searchtype='accurate', limit=50)
            #    except APICallTimeoutError as e:
            #        print(f'({tries}) Timeout error getting weather observations, trying again...')
            #        print(str(e))
            
            curr_coords = (float(latitude), float(longitude))
            # Find observation closest to coordinates
            # TODO: speed this up?
            #observation = min(observations, \
            #    key=lambda x: get_distance(curr_coords, (x.get_location().get_lat(), x.get_location().get_lon())))
            print(f'city: {city}')
            print(f'country: {country}')
            try:
                observation = owm.weather_at_place(f'{city},{country}')
            except NotFoundError:
                city, country = get_location_by_city(city, country)
                observation = owm.weather_at_place(f'{city},{country}')
            city_id = observation.get_location().get_ID()

        w = observation.get_weather()

        context = {
            'latitude': latitude,
            'longitude': longitude,
            'city': city,
            'country': country,
            'wind': w.get_wind(),
            'humidity': w.get_humidity(),
            'temperature': w.get_temperature('fahrenheit'),
            'status': w.get_status(),
            'details': w.get_detailed_status().capitalize(),
            'code': w.get_weather_code(),
            'time_of_day': time_of_day,
        }
        return JsonResponse(context) 

MAPQUEST_CITY_ID = 'adminArea5'
MAPQUEST_COUNTRY_ID = 'adminArea1'

def get_location(lat, lon):
    url = f'http://www.mapquestapi.com/geocoding/v1/reverse?key={settings.MAPQUEST_KEY}' + \
        f'&location={lat},{lon}&includeRoadMetadata=true&includeNearestIntersection=true'

    response = urlopen(url).read()
    j = json.loads(response)
    components = j['results'][0]['locations'][0]
    city = components[MAPQUEST_CITY_ID]
    country = components[MAPQUEST_COUNTRY_ID]
    """
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    """
    return city, country

def get_location_by_city(city, country):
    location_query = quote(f'{city},{country}')
    url = f'http://open.mapquestapi.com/geocoding/v1/address?key={settings.MAPQUEST_KEY}&location={location_query}'
    print(f'url: {url}')

    response = urlopen(url).read()
    j = json.loads(response)
    components = j['results'][0]['locations'][0]
    city = components[MAPQUEST_CITY_ID]
    country = components[MAPQUEST_COUNTRY_ID]

    return city, country

def get_timezone(lat, lon):
    #url = f'http://api.geonames.org/timezoneJSON?lat={lat}&lng={lon}&username={settings.GEONAMES_USERNAME}'

    #response = urlopen(url).read()
    #j = json.loads(response)
    utc_offset = -5#j['rawOffset']

    return utc_offset

# Only accurate for relatively short distances
def get_distance(coords1, coords2):
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    x = math.radians(lon1 - lon2) * math.cos(math.radians(lat1))
    y = math.radians(lat1 - lat2)
    dist = math.sqrt(x**2 + y**2)
    return dist

def update_weather(request, module):
    instance = Weather.objects.filter(module=module).first()
    form = WeatherForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('user-modules')
    context = {
        'module_form': form,
        'module_type': 'weather'
    }
    return render(request, 'dashboard/update_form.html', context)