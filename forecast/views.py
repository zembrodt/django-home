from django.shortcuts import redirect, render
from django.conf import settings
from django.http.response import JsonResponse
from django.template.loader import get_template
from pyowm.exceptions.api_call_error import APICallTimeoutError
from urllib.request import urlopen
from datetime import datetime, timedelta
from dashboard.models import Module
from .models import Forecast
from .forms import ForecastForm
from weather.views import (
    get_location,
    get_timezone,
    get_distance,
)
import json, math, pyowm

owm = pyowm.OWM(settings.OWM_KEY)

# NOTE: placeholder
def forecast(request, module):
    #forecast = Forecast.objects.get(module=module)
    template = get_template('forecast/forecast.html')
    context = {
        'id': module.id
    }
    return template.render(context)

def update_forecast_stats(request):
    if request.method == 'GET':
        module_id = request.GET.get('id')
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')

        module = Module.objects.get(pk=module_id)
        forecast = Forecast.objects.get(module=module)

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
            hour_forecast = owm.three_hours_forecast_at_id(city_id)
            start_time = hour_forecast.when_starts(timeformat='date')
            end_time = hour_forecast.when_ends(timeformat='date')
            print(f'hour forecast start: {start_time}\nhour forecast end: {end_time}')
            forecasts = hour_forecast.get_forecast()
            print(f'num of forecasts: {forecasts.count_weathers()}')
            my_forecasts = []
            cap_forecast = True if forecast.length >= 0 else False
            time_start = None
            time_end = None
            weathers = forecasts.get_weathers()
            for i, w in enumerate(weathers):
                if i >= forecast.length and cap_forecast:
                    break
                w_time = w.get_reference_time(timeformat='date') + timedelta(hours=utc_offset)
                if i == 0:
                    time_start = w_time
                elif (i+1 >= forecast.length and cap_forecast) or i+1 >= len(weathers):
                    time_end = w_time
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
        print(f'time start: {time_start}')
        print(f'time end: {time_end}')
        print(f'city: {city}')
        print(f'country: {country}')

        context = {
            'latitude': latitude,
            'longitude': longitude,
            'city': city,
            'country': country,
            'time_start': time_start,
            'time_end': time_end,
            'forecasts': my_forecasts
        }
        return JsonResponse(context)

def update_forecast(request, module):
    instance = Forecast.objects.filter(module=module).first()
    form = ForecastForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('user-modules')
    context = {
        'module_form': form,
        'module_type': 'Forecast'
    }
    return render(request, 'dashboard/update_form.html', context)