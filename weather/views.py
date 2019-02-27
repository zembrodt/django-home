from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    UpdateView,
)
from pyowm.exceptions.api_call_error import APICallTimeoutError
from urllib.request import urlopen
from datetime import datetime, timedelta
from dashboard.models import Module
from dashboard.forms import (
    WeatherForm
)
from .models import Weather
import json, math, pyowm

MAPQUEST_KEY = 'fQlDAwzUnxmZlLuaA4Q1o9vpsqHdL8PK'
GEONAMES_USERNAME = 'zembrodt'
owm = pyowm.OWM('6144810fddc53644a589937de8d3ea15')

#observation = owm.weather_at_place('Lexington,US')
#w = observation.get_weather()

# NOTE: placeholder
def weather(request, module):
    weather = Weather.objects.get(module=module)
    template = get_template('weather/weather.html')
    context = {
        'id': module.id,
        'forecast': weather.show_forecast
    }
    return template.render(context)

"""
def home(request):
    # Default location
    observation = owm.weather_at_place('London,UK')
    loc = observation.get_location()
    w = observation.get_weather()

    # Specify what modules to include in the dashboard
    modules = ['dt', 'weather']

    context = {
        'latitude': loc.get_lat(),
        'longitude': loc.get_lon(),
        'city': 'London',
        'country': 'UK',
        'wind': w.get_wind(),
        'humidity': w.get_humidity(),
        'temperature': w.get_temperature('fahrenheit'),
        'status': w.get_status(),
        'details': w.get_detailed_status(),
        'code': w.get_weather_code(),
        'modules': modules
    }
    return render(request, 'dashboard/dashboard.html', context)
"""
def update_weather_stats(request):
    if request.method == 'GET':
        module_id = request.GET.get('id')
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')

        module = Module.objects.get(pk=module_id)
        weather = Weather.objects.get(module=module)

        print(f'latitude: {latitude}\nlongitude: {longitude}')

        city = 'London'
        country = 'UK'
        observation = None
        if latitude is None or longitude is None:
            # Default location
            observation = owm.weather_at_place('London,UK')
        else:
            print('we got here!')
            
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
            observation = owm.weather_at_place(f'{city},{country}')
            city_id = observation.get_location().get_ID()

            # Calculate forecasts
            if weather.show_forecast:
                hour_forecast = owm.three_hours_forecast_at_id(city_id)
                start_time = hour_forecast.when_starts(timeformat='date')
                end_time = hour_forecast.when_ends(timeformat='date')
                print(f'hour forecast start: {start_time}\nhour forecast end: {end_time}')
                forecasts = hour_forecast.get_forecast()
                print(f'num of forecasts: {forecasts.count_weathers()}')
                my_forecasts = []
                cap_forecast = True if weather.forecast_length >= 0 else False
                i = 0
                for w in forecasts.get_weathers():
                    if i >= weather.forecast_length and cap_forecast:
                        break
                    w_time = w.get_reference_time(timeformat='date') + timedelta(hours=utc_offset)
                    w_temp = w.get_temperature(unit='fahrenheit')
                    w_status = w.get_status()
                    w_code = w.get_weather_code()
                    print(w_time.hour)
                    print(f'UTC offset: {utc_offset}')
                    w_time_of_day = 'day' if w_time.hour >= 7 and w_time.hour < 20 else 'night'
                    print(f'Forecast at: {w_time}\n\ttemp: {w_temp}\n\tstatus: {w_status}\n\tcode: {w_code}')
                    my_forecasts.append({
                        'time': w_time,
                        'temp': w_temp,
                        'status': w_status,
                        'code': w_code,
                        'time_of_day': w_time_of_day
                    })
                    i += 1

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
            'details': w.get_detailed_status(),
            'code': w.get_weather_code(),
            'time_of_day': time_of_day,
        }
        if weather.show_forecast:
            context['forecasts'] = my_forecasts
        return JsonResponse(context) 

def get_location(lat, lon):
    url = f'http://www.mapquestapi.com/geocoding/v1/reverse?key={MAPQUEST_KEY}' + \
        f'&location={lat},{lon}&includeRoadMetadata=true&includeNearestIntersection=true'

    response = urlopen(url).read()
    j = json.loads(response)
    components = j['results'][0]['locations'][0]
    city = components['adminArea5']
    country = components['adminArea1']
    """
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
    """
    return city, country

def get_timezone(lat, lon):
    #url = f'http://api.geonames.org/timezoneJSON?lat={lat}&lng={lon}&username={GEONAMES_USERNAME}'

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
        'module_type': 'Weather'
    }
    return render(request, 'dashboard/update_form.html', context)