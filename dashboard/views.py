from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    CreateView,
)
from django.template.loader import get_template
from users.models import Profile
from dashboard.models import Module
from dt import views as dt_views
from photos import views as photos_views
from weather import views as weather_views
from .forms import (
    ModuleCreateForm,
    DateForm,
    WeatherForm
)
import json, re

DEFAULT_Z_INDEX = 9

def home(request):
    context = {
        'user': request.user
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def dashboard(request):
    context = {
        'modules': generate_context(request),
        'user': request.user
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def update(request):
    context = {
        'modules': generate_context(request),
        'user': request.user
    }
    return render(request, 'dashboard/dashboard_update.html', context)

@login_required
def save_update(request):
    if request.method == 'GET':
        id_data = request.GET.getlist('id_data[]')

        user = Profile.objects.filter(user=request.user).first()

        for data_json in id_data:
            print(f'data_json: {data_json}')
            
            data = json.loads(data_json)
            t, pk = data['id'].split('-')
            print(f't: {t}\npk: {pk}')
            
            module = Module.objects.filter(pk=pk, owner=user).first()
            module.x = int(re.sub('px', '', data['left']))
            module.y = int(re.sub('px', '', data['top']))
            print(f'updated module: {module}')
            module.save()
            
            #module.update(x=int(re.sub('px', '', data['top'])), y=int(re.sub('px', '', data['left'])))

        context = {
            'blah': 'blah'
        }
        return JsonResponse(context)

    # TODO no valid return if method isn't GET

class ModuleListView(LoginRequiredMixin, ListView):#UserPassesTestMixin, ListView):
    model = Module
    template_name = 'dashboard/modules.html' # default: <app>/<model>_<viewtype>.html
    context_object_name = 'modules'
    
    #def get(self, request, *args, **kwargs):
    #    context = super(ModuleListView, self).get_context_data(**kwargs)
    #    context.update({'title': f'{self.request.user}\'s Modules'})

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        profile = Profile.objects.filter(user=user).first()
        #return Profile.objects.filter(user=user).first().modules.all()
        return Module.objects.filter(owner=profile)
    '''
    def test_func(self):
        #post = self.get_object()
        # TODO: update modules to store their author
        if self.request.user == self.kwargs.get('username'): #post.author:
            return True
        return False
    '''

class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    fields = ['module_type', 'x', 'y']
    title = 'Add Module'

    def form_valid(self, form):
        user = Profile.objects.filter(user=self.request.user).first()
        form.instance.owner = user
        return super().form_valid(form)

def module_create(request):
    if request.is_ajax():
        if request.method == 'GET':
            module_type = request.GET.get('module_type')
            # NOTE: do this with actual ids later
            form_render = None
            if module_type == 'Datetime':
                dt_form = DateForm()
                template = get_template('dt/dt_form.html')
                context = {
                    'dt_form': dt_form
                }
                form_render = template.render(context)
            elif module_type == 'Weather':
                weather_form = WeatherForm()
                template = get_template('weather/weather_form.html')
                context = {
                    'weather_form': weather_form
                }
                form_render = template.render(context)
            else:
                # What do here?
                form_render = None
            context = {
                'extended_form': form_render
            }
            return JsonResponse(context)
    if request.method == 'POST':
        module_form = ModuleCreateForm(request.POST)
        if module_form.is_valid():
            module_type = module_form.cleaned_data['module_type']
            module = module_form.save(commit=False)
            user = Profile.objects.get(user=request.user)
            print(f'We have a module! {module}')
            print(f'Type is: \'{module_type}\'')
            #extended_form = None
            # NOTE: this is also temporary, use actual module ids
            if str(module_type) == 'Datetime':
                print('we got here')
                dt_form = DateForm(request.POST)#, module=module)#, instance=module)
                if dt_form.is_valid():
                    dt = dt_form.save(commit=False)
                    module.owner = user
                    module.save()
                    dt.module = module
                    dt.save()
                    print(f'We have DT module! {dt}')
                else:
                    print('Form was not valid')
            elif str(module_type) == 'Weather':
                weather_form = WeatherForm(request.POST)#, module=module)#, instance=module)
                if weather_form.is_valid():
                    weather = weather_form.save(commit=False)
                    module.owner = user
                    module.save()
                    weather.module = module
                    weather.save()
                    print(f'We have Weather module! {weather}')
            else:
                # TODO: what do?
                pass
            return redirect('user-modules') # Can also redirect to an object's get_absolute_url()
    else:
        module_form = ModuleCreateForm()
    context = {
        'module_form': module_form
    }
    return render(request, 'dashboard/module_form.html', context)


def generate_context(request):
    user = Profile.objects.filter(user=request.user).first()
    modules = {}
    z_index = DEFAULT_Z_INDEX # TODO: store this value in module settings?
    for module in Module.objects.filter(owner=user):
        t = module.module_type.module_type
        # TODO: may need to assign this dict key to pk of module to allow multiple copies
        page_render = None
        if t == 'dt':
            page_render = dt_views.dt(request, module)
        elif t == 'photos':
            page_render = photos_views.photos(request, module)
        elif t == 'weather':
            page_render = weather_views.weather(request, module)

        print(f'page_render: {page_render}')

        modules[module.id] = {
            'id': module.id,
            'type': t,
            'styles': f'{t}/includes/{t}_styles.html',
            'scripts': f'{t}/includes/{t}_scripts.html',
            #'page': f'{t}/{t}.html',
            'top': module.y,
            'left': module.x,
            'z_index': z_index,
            'content': page_render,
        }
        z_index += 1
    return modules

# Module-specific gets
