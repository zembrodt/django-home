from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
)
from users.models import Profile
from dashboard.models import Module
import json, re

# Specify what modules to include in the dashboard
# TODO: add to user settings
"""
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
"""

def home(request):
    context = {
        'modules': generate_context(request.user),
        'user': request.user
    }
    return render(request, 'dashboard/dashboard.html', context)

def update(request):
    context = {
        'modules': generate_context(request.user),
        'user': request.user
    }
    return render(request, 'dashboard/dashboard_update.html', context)

def save_update(request):
    if request.method == 'GET':
        id_data = request.GET.getlist('id_data[]')

        user = Profile.objects.filter(user=request.user).first()

        for data_json in id_data:
            # TODO: may need to update if PKs are used
            data = json.loads(data_json)
            i = data['id']
            module = user.modules.filter(module_type=i).first() #NOTE: not pk
            module.x = int(re.sub('px', '', data['left']))
            module.y = int(re.sub('px', '', data['top']))
            module.save()
            #module.update(x=int(re.sub('px', '', data['top'])), y=int(re.sub('px', '', data['left'])))

        context = {
            'blah': 'blah'
        }
        return JsonResponse(context)

    # TODO no valid return if method isn't GET

class ModulesListView(ListView):#UserPassesTestMixin, ListView):
    model = Module
    template_name = 'dashboard/modules.html' # default: <app>/<model>_<viewtype>.html
    context_object_name = 'modules'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Profile.objects.filter(user=user).first().modules.all()
    '''
    def test_func(self):
        #post = self.get_object()
        # TODO: update modules to store their author
        if self.request.user == self.kwargs.get('username'): #post.author:
            return True
        return False
    '''

def generate_context(user):
    user = Profile.objects.filter(user=user).first()
    modules = {}
    for module in user.modules.all():
        name = module.module_type
        # TODO: may need to assign this dict key to pk of module to allow multiple copies
        modules[name] = {
            'id': name,
            'styles': f'{name}/includes/{name}_styles.html',
            'scripts': f'{name}/includes/{name}_scripts.html',
            'page': f'{name}/{name}.html',
            'top': module.y,
            'left': module.x
        }
    return modules