from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView
)
from django.template.loader import get_template
from django.templatetags.static import static
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
from photos.forms import ImageForm, PhotosForm, ImageFormSet
from photos.models import Image, Photos
import json, re

def home(request):
    context = {
        'user': request.user
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def dashboard(request):
    modules, unique_modules = generate_context(request)
    context = {
        'modules': modules,
        'unique_modules': unique_modules,
        'user': request.user
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def update(request):
    modules, unique_modules = generate_context(request)
    context = {
        'modules': modules,
        'unique_modules': unique_modules,
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
            _, t, pk = data['id'].split('-')
            print(f't: {t}\npk: {pk}')
            
            module = Module.objects.filter(pk=pk, owner=user).first()
            module.x = int(re.sub('px', '', data['left']))
            module.y = int(re.sub('px', '', data['top']))
            module.z_index = int(data['z-index'])
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

'''
class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    fields = ['module_type', 'x', 'y']
    title = 'Add Module'

    def form_valid(self, form):
        user = Profile.objects.filter(user=self.request.user).first()
        form.instance.owner = user
        return super().form_valid(form)
'''

class ModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Module

    def test_func(self):
        module = self.get_object()
        return self.request.user.profile == module.owner
    
    def get_success_url(self):
        return reverse('user-modules')

def module_create(request):
    if request.is_ajax():
        if request.method == 'GET':
            module_type = request.GET.get('module_type')
            # NOTE: do this with actual ids later
            form_render = None
            form_script = None
            if module_type == 'Datetime':
                dt_form = DateForm()
                template = get_template('dt/dt_form.html')
                context = {
                    'dt_form': dt_form
                }
                form_render = template.render(context)
            elif module_type == 'Photos':
                photos_form = PhotosForm()
                formset = ImageFormSet(queryset=Image.objects.none())
                template = get_template('photos/photos_form.html')
                context = {
                    'photos_form': photos_form,
                    'formset': formset
                }
                form_render = template.render(context)
                form_script = 'photos/scripts/photos_form.js'
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
                'extended_form': form_render,
                'extended_script': static(form_script)
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
            if str(module_type) == 'Photos':
                photos_form = PhotosForm(request.POST)#, module=module)#, instance=module)
                formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
                if photos_form.is_valid() and formset.is_valid():
                    photos = photos_form.save(commit=False)
                    module.owner = user
                    module.save()
                    photos.module = module
                    photos.save()
                    print(f'We have Photos module! {photos}')
                    for form in formset.cleaned_data:
                        print('We are in the formset!')
                        print(f'form: {form}')
                        #this helps to not crash if the user   
                        #do not upload all the photos
                        if form:
                            image_form = form['image']
                            print(f'image_form: {image_form}')
                            image = Image(photos_module=photos, image=image_form)
                            print(f'image: {image}')
                            image.save()
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

def module_update(request, **kwargs):
    module = get_object_or_404(Module, id=kwargs['pk'])
    #module = Module.objects.filter(pk=kwargs['pk']).first()
    # TODO: check if this module is owned by the user?
    t = module.module_type.module_type
    if t == 'dt':
        return dt_views.update_dt(request, module)
    elif t == 'photos':
        return photos_views.update_photos(request, module)
    elif t == 'weather':
        return weather_views.update_weather(request, module)
    else:
        # TODO: return a 404 page
        pass

def generate_context(request):
    user = Profile.objects.filter(user=request.user).first()
    modules = {}
    unique_modules = []
    for module in Module.objects.filter(owner=user):
        moveable = True
        t = module.module_type.module_type
        if t not in unique_modules:
            unique_modules.append(t)
        # TODO: may need to assign this dict key to pk of module to allow multiple copies
        page_render = None
        if t == 'dt':
            page_render = dt_views.dt(request, module)
        elif t == 'photos':
            page_render = photos_views.photos(request, module)
            if Photos.objects.filter(module=module).first().is_background:
                moveable = False
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
            'z_index': module.z_index,
            'text_color': module.text_color,
            'moveable': moveable,
            'content': page_render,
        }
    return modules, unique_modules

# Module-specific gets
