from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    CreateView,
)
from users.models import Profile
from dashboard.models import Module
import json, re

@login_required
def home(request):
    context = {
        'modules': generate_context(request.user),
        'user': request.user
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def update(request):
    context = {
        'modules': generate_context(request.user),
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

    def form_valid(self, form):
        user = Profile.objects.filter(user=self.request.user).first()
        form.instance.owner = user
        return super().form_valid(form)

def generate_context(user):
    user = Profile.objects.filter(user=user).first()
    modules = {}
    for module in Module.objects.filter(owner=user):
        t = module.module_type.module_type
        # TODO: may need to assign this dict key to pk of module to allow multiple copies
        modules[module.id] = {
            'id': module.id,
            'type': t,
            'styles': f'{t}/includes/{t}_styles.html',
            'scripts': f'{t}/includes/{t}_scripts.html',
            'page': f'{t}/{t}.html',
            'top': module.y,
            'left': module.x
        }
    return modules