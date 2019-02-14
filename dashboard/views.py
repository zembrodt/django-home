from django.shortcuts import render

def home(request):

    # Specify what modules to include in the dashboard
    # TODO: add to user settings
    modules = [
        {
            'id': 'dt',
            'styles': 'dt/includes/dt_styles.html',
            'scripts': 'dt/includes/dt_scripts.html',
            'page': 'dt/dt.html',
            'top': 200,
            'left': 10
        },
        {
            'id': 'weather',
            'styles': 'weather/includes/weather_styles.html',
            'scripts': 'weather/includes/weather_scripts.html',
            'page': 'weather/weather.html',
            'top': 50,
            'left': 100
        }
    ]

    context = {
        'modules': modules
    }
    return render(request, 'dashboard/dashboard.html', context)

def update(request):
    # TODO: add to user settings
    modules = [
        {
            'id': 'dt',
            'styles': 'dt/includes/dt_styles.html',
            'scripts': 'dt/includes/dt_scripts.html',
            'page': 'dt/dt.html',
            'top': 200,
            'left': 10
        },
        {
            'id': 'weather',
            'styles': 'weather/includes/weather_styles.html',
            'scripts': 'weather/includes/weather_scripts.html',
            'page': 'weather/weather.html',
            'top': 50,
            'left': 100
        }
    ]

    context = {
        'modules': modules
    }
    return render(request, 'dashboard/dashboard_update.html', context)

def save_update(request):
    pass