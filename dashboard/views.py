from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.template.loader import get_template
from django.templatetags.static import static
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView
)
from users.models import Profile
from .forms import ModuleCreateForm
from .models import Module
from dt import views as dt_views
from dt.forms import DateForm
from forecast.forms import ForecastForm
from forecast.models import Forecast
from forecast import views as forecast_views
from photos.forms import ImageForm, PhotosForm, ImageFormSet
from photos.models import Image, Photos
from photos import views as photos_views
from weather.forms import WeatherForm
from weather import views as weather_views
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from .serializers import ModuleSerializer
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)

import json
import re

class ModuleAccessPermission(BasePermission):
    message = 'Updating/Deleting modules is not allowed'

    def has_object_permission(self, request, view, obj):
        print(f'Checking for permissions! user: {request.user}')
        return request.user == obj.owner

class ModuleListAPIView(ListAPIView):
    serializer_class = ModuleSerializer
    permission_classes = (ModuleAccessPermission, )

    def get_queryset(self):
        user = Profile.objects.get(user=self.request.user)
        return Module.objects.filter(owner=user)

@api_view(['PUT'])
@permission_classes((IsAuthenticated, ModuleAccessPermission))
def module_update_view(request, **kwargs):
    print(f'request data: {request.data}')
    module = get_object_or_404(Module, id=kwargs['pk'])
    serializer = ModuleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.update(module, request.data)
        print('Update passed!')
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ModuleAccessPermission))
def module_create_view(request):
    print(f'request data: {request.data}')
    serializer = ModuleSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.create(request.data)
        print('Update passed!')
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class ModuleDeleteAPIView(DestroyAPIView):
    serializer_class = ModuleSerializer
    permission_classes = (ModuleAccessPermission, )

    def get_queryset(self):
        user = Profile.objects.get(user=self.request.user)
        return Module.objects.filter(owner=user)

'''
class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny, )
'''
#@login_required
@api_view(['GET'])
@authentication_classes((TokenAuthentication,SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated, ModuleAccessPermission))
def modules(request):
    print(f'We\'re in modules! user: {request.user}')
    user = Profile.objects.get(user=request.user)
    #data = [ModuleSerializer(module).data for module in modules]
    data = {'modules': [ModuleSerializer(module).data for module in Module.objects.filter(owner=user)] }
    return Response(data)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ModuleAccessPermission))
def module(request, **kwargs):
    module = get_object_or_404(Module, id=kwargs['pk'])
    data = {'module': ModuleSerializer(module).data}
    return Response(data)
    

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
            data = json.loads(data_json)
            _, t, pk = data['id'].split('-')

            module = Module.objects.filter(pk=pk, owner=user).first()
            module.x = int(re.sub('px', '', data['left']))
            module.y = int(re.sub('px', '', data['top']))
            module.z_index = int(data['z-index'])
            module.save()

            #module.update(x=int(re.sub('px', '', data['top'])), y=int(re.sub('px', '', data['left'])))

        context = {
            'blah': 'blah'
        }
        return JsonResponse(context)

    # TODO no valid return if method isn't GET


# UserPassesTestMixin, ListView):
class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    # default: <app>/<model>_<viewtype>.html
    template_name = 'dashboard/modules.html'
    context_object_name = 'modules'

    # def get(self, request, *args, **kwargs):
    #    context = super(ModuleListView, self).get_context_data(**kwargs)
    #    context.update({'title': f'{self.request.user}\'s Modules'})

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        profile = Profile.objects.filter(user=user).first()
        # return Profile.objects.filter(user=user).first().modules.all()
        return Module.objects.filter(owner=profile)
    '''
    def test_func(self):
        #post = self.get_object()
        # TODO: update modules to store their author
        if self.request.user == self.kwargs.get('username'): #post.author:
            return True
        return False
    '''


def api_modules(request):
    print(f'request: {request}')
    print(f'user: {request.user}')
    return JsonResponse({'blah1': 'blah1', 'blah2': 'blah2'})


def get_extended_form(request):
    if request.method == 'GET':
        module_type = request.GET.get('module_type')
        form_render = None
        form_script = None
        if module_type == 'Datetime':
            dt_form = DateForm()
            template = get_template('dt/dt_form.html')
            context = {
                'dt_form': dt_form
            }
            form_render = template.render(context)
        elif module_type == 'Forecast':
            forecast_form = ForecastForm()
            template = get_template('forecast/forecast_form.html')
            context = {
                'forecast_form': forecast_form
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
            'extended_script': static(form_script) if form_script else ''
        }
        return JsonResponse(context)


def module_create(request):
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
            extended_form = None
            extended_module = None
            if str(module_type) == 'Datetime':
                extended_form = DateForm(request.POST)
            elif str(module_type) == 'Forecast':
                extended_form = ForecastForm(request.POST)
            elif str(module_type) == 'Photos':
                extended_form = PhotosForm(request.POST)
                formset = ImageFormSet(
                    request.POST, request.FILES, queryset=Image.objects.none())
                if extended_form.is_valid() and formset.is_valid():
                    extended_module = extended_form.save(commit=False)
                    for form in formset.cleaned_data:
                        # prevent crashing if the user doesn't upload all the photos
                        if form:
                            image_form = form['image']
                            public = form['public']
                            image = Image(
                                owner=user, photos_module=extended_module, image=image_form, public=public)
                            image.save()
            elif str(module_type) == 'Weather':
                extended_form = WeatherForm(request.POST)
            else:
                pass

            # Temporary save the module if it wasn't saved above
            if extended_form.is_valid() and extended_module is None:
                extended_module = extended_form.save(commit=False)
            # Save all data from the form
            if extended_form.is_valid():
                module.owner = user
                module.save()
                extended_module.module = module
                extended_module.save()
            # TODO: complete this
            module_style = get_template('dashboard/includes/module_style.html')
            module_content = get_template(
                'dashboard/includes/module_content.html')
            page_content = get_content(request, module)
            update_method = get_update_method(module)
            module_script = get_template(
                'dashboard/includes/module_script.html')
            context = {
                'id': module.id,
                'type': module.module_type.module_type,
                # NOTE: adding a style tag to head may not work, may need to put this as a 'style' within the div
                # it seems to work, however
                'style': module_style.render({
                    'id': module.id,
                    'type': module.module_type.module_type,
                    'values': {
                        'z-index': module.z_index,
                        'top': module.y,
                        'left': module.x,
                        'color': module.text_color,
                    },
                }),   # Module's style
                'content': module_content.render({
                    'id': module.id,
                    'type': module.module_type.module_type,
                    'content': page_content['content'],
                    'moveable': page_content['moveable'],
                    'ajax': True,
                    'values': {
                        'zindex': module.z_index,
                        'top': module.y,
                        'left': module.x,
                        'color': module.text_color,
                    }
                }),  # Module's div
                'values': {
                    'zindex': module.z_index,
                    'top': module.y,
                    'left': module.x,
                    'color': module.text_color,
                    'moveable': page_content['moveable'],
                },
                'script': module_script.render({

                }),  # Module's script
                'method': update_method,
            }
            return JsonResponse(context)
            '''
                if dt_form.is_valid():
                    dt = dt_form.save(commit=False)
                    module.owner = user
                    module.save()
                    dt.module = module
                    dt.save()
                    print(f'We have DT module! {dt}')
                else:
                    print('Form was not valid')
            elif str(module_type) == 'Forecast':
                forecast_form = ForecastForm(request.POST)
                if forecast_form.is_valid():
                    forecast = forecast_form.save(commit=False)
                    module.owner = user
                    module.save()
                    forecast.module = module
                    forecast.save()
                    print(f'We have Forecast module! {forecast}')
                else:
                    print('Form was not valid')
            elif str(module_type) == 'Photos':
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
                        # prevent crashing if the user doesn't upload all the photos
                        if form:
                            image_form = form['image']
                            public = form['public']
                            image = Image(owner=user, photos_module=photos, image=image_form, public=public)
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
            '''
            # return redirect('user-modules') # Can also redirect to an object's get_absolute_url()
    else:
        module_form = ModuleCreateForm()
    context = {
        'module_form': module_form
    }
    template = get_template('dashboard/add_module.html')
    return JsonResponse({'content': template.render(context, request=request)})
    # return render(request, 'dashboard/module_form.html', context)


def module_update(request, **kwargs):
    module = get_object_or_404(Module, id=kwargs['pk'])
    if request.user.profile == module.owner:
        #module = Module.objects.filter(pk=kwargs['pk']).first()
        # TODO: check if this module is owned by the user?
        t = module.module_type.module_type
        render = None
        method = None
        if t == 'dt':
            render, method = dt_views.update_dt(request, module)
        elif t == 'forecast':
            render, method = forecast_views.update_forecast(request, module)
        elif t == 'photos':
            render, method = photos_views.update_photos(request, module)
        elif t == 'weather':
            render, method = weather_views.update_weather(request, module)
        else:
            # TODO: return a 404 page
            pass

        # Check if this was an AJAX call or not
        # if request.is_ajax():
        print(f'ajax render: {render}')
        return JsonResponse({'content': render, 'method': method})


def module_delete(request, **kwargs):
    module = get_object_or_404(Module, id=kwargs['pk'])
    print(f'Module to delete: {module}')
    if request.user.profile == module.owner:
        if request.is_ajax():
            if request.method == 'POST':
                module.delete()
                return JsonResponse({'blah': 'blah'})
            else:
                context = {
                    'id': module.id,
                    'module_type': module.module_type.module_type
                }
                template = get_template('dashboard/delete_form.html')
                return JsonResponse({'content': template.render(context, request=request)})


def generate_context(request):
    user = Profile.objects.filter(user=request.user).first()
    modules = {}
    unique_modules = []
    for module in Module.objects.filter(owner=user):
        module_type = module.module_type.module_type
        if module_type not in unique_modules:
            unique_modules.append(module_type)

        page_content = get_content(request, module)

        modules[module.id] = {
            'id': module.id,
            'type': module_type,
            'styles': f'{module_type}/includes/{module_type}_styles.html',
            'scripts': f'{module_type}/includes/{module_type}_scripts.html',
            # 'page': f'{module_type}/{module_type}.html',
            'top': module.y,
            'left': module.x,
            'z_index': module.z_index,
            'text_color': module.text_color,
            'moveable': page_content['moveable'],
            'content': page_content['content'],
        }
    return modules, unique_modules


def get_content(request, module):
    module_type = module.module_type.module_type
    moveable = True
    page_render = None
    # TODO: may need to assign this dict key to pk of module to allow multiple copies
    if module_type == 'dt':
        page_render = dt_views.dt(request, module)
    elif module_type == 'forecast':
        page_render = forecast_views.forecast(request, module)
    elif module_type == 'photos':
        page_render = photos_views.photos(request, module)
        if Photos.objects.filter(module=module).first().is_background:
            moveable = False
    elif module_type == 'weather':
        page_render = weather_views.weather(request, module)
    return {
        'content': page_render,
        'moveable': moveable,
    }


def get_update_method(module):
    module_type = module.module_type.module_type
    if module_type == 'dt':
        return 'update_dt'
    elif module_type == 'forecast':
        return 'update_forecast'
    elif module_type == 'photos':
        return 'update_photos'
    elif module_type == 'weather':
        return 'update_weather'

# Module-specific gets
