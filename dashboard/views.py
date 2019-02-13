from django.shortcuts import render

def home(request):

    # Specify what modules to include in the dashboard
    # TODO: add to user settings
    modules = [
        {
            'id': 'dt',
            'top': 0,
            'left': 0
        },
        {
            'id': 'weather',
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
            'top': 0,
            'left': 0
        },
        {
            'id': 'weather',
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