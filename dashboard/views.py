from django.shortcuts import render
from django.http.response import JsonResponse
import json

# Specify what modules to include in the dashboard
# TODO: add to user settings
modules = {
        'dt': {
            'id': 'dt',
            'styles': 'dt/includes/dt_styles.html',
            'scripts': 'dt/includes/dt_scripts.html',
            'page': 'dt/dt.html',
            'top': 200,
            'left': 10
        },
        'weather': {
            'id': 'weather',
            'styles': 'weather/includes/weather_styles.html',
            'scripts': 'weather/includes/weather_scripts.html',
            'page': 'weather/weather.html',
            'top': 50,
            'left': 100
        }
}

def home(request):
    context = {
        'modules': modules
    }
    return render(request, 'dashboard/dashboard.html', context)

def update(request):
    context = {
        'modules': modules
    }
    return render(request, 'dashboard/dashboard_update.html', context)

def save_update(request):
    if request.method == 'GET':
        id_data = request.GET.getlist('id_data[]')

        """
        for data_json in id_data:
            data = json.loads(data_json)
            i = data['id']
            modules[i]['top'] = int(data['top'])
            modules[i]['left'] = int(data['left'])
        print(f'New modules:\n{modules}')
        """
        context = {
            'blah': 'blah'
        }
        return JsonResponse(context)

    # TODO no valid return if method isn't GET