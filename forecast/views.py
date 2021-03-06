from django.shortcuts import redirect, render
from django.conf import settings
from django.http.response import JsonResponse
from django.template.loader import get_template
from pyowm.exceptions.api_call_error import APICallTimeoutError
from urllib.request import urlopen
from datetime import datetime, timedelta
from dashboard.forms import ModuleUpdateForm
from dashboard.models import Module
from .models import Forecast
from .forms import ForecastForm
from weather.views import (
    get_location,
    get_timezone,
    get_distance,
)
from weather.forms import UNIT_DISPLAY
import json, math, pyowm, time

owm = pyowm.OWM(settings.OWM_KEY)

# NOTE: placeholder
def forecast(request, module):
    forecast = Forecast.objects.get(module=module)
    template = get_template('forecast/forecast.html')
    context = {
        'id': module.id,
        'forecast_length': range(forecast.length),
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
            
            #now = utc_now + timedelta(hours=utc_offset)

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
            forecasts = hour_forecast.get_forecast()
            my_forecasts = []
            cap_forecast = True if forecast.length >= 0 else False
            for i, w in enumerate(forecasts.get_weathers()):
                if i >= forecast.length and cap_forecast:
                    break
                w_time = w.get_reference_time(timeformat='date') + timedelta(hours=utc_offset)
                w_temp = w.get_temperature(unit=forecast.unit)
                w_status = w.get_status()
                w_code = w.get_weather_code()
                w_time_of_day = 'day' if w_time.hour >= 7 and w_time.hour < 20 else 'night'
                my_forecasts.append({
                    'time': int(time.mktime(w_time.timetuple())) * 1000,
                    'temp': w_temp,
                    'status': w_status,
                    'code': w_code,
                    'time_of_day': w_time_of_day
                })
        start_time = my_forecasts[0]['time']
        end_time = my_forecasts[-1]['time']
        print(f'time start: {start_time}')
        print(f'time end: {end_time}')
        print(f'city: {city}')
        print(f'country: {country}')

        context = {
            'latitude': latitude,
            'longitude': longitude,
            'city': city,
            'country': country,
            'unit': UNIT_DISPLAY[forecast.unit],
            #'time_start': start_time,
            #'time_end': end_time,
            'forecasts': my_forecasts
        }
        return JsonResponse(context)

def update_forecast(request, module):
    instance = Forecast.objects.filter(module=module).first()
    module_form = ModuleUpdateForm(request.POST or None, instance=module)
    forecast_form = ForecastForm(request.POST or None, instance=instance)
    if module_form.is_valid() and forecast_form.is_valid():
        module_form.save()
        forecast_form.save()
        if request.is_ajax():
            return forecast(request, module), 'update_forecast'
        else:
            return redirect('user-modules')
    context = {
        'id': module.id,
        'module_form': module_form,
        'extended_form': forecast_form,
        'module_type': 'forecast'
    }
    if request.is_ajax():
        form = get_template('dashboard/update_form_embedded.html')
        return form.render(context, request=request), ''
    else:
        return render(request, 'dashboard/update_form.html', context)