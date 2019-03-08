from django.shortcuts import redirect, render
from django.template.loader import get_template
from .forms import DateForm
from .models import Datetime
from dashboard.forms import ModuleUpdateForm

# NOTE: placeholder
def dt(request, module):
    template = get_template('dt/dt.html')
    datetime = Datetime.objects.filter(module=module).first()
    context = {
        'id': module.id,
        'twenty_four_hours': 1 if datetime.twenty_four_hours is True else 0
    }
    return template.render(context)

def update_dt(request, module):
    instance = Datetime.objects.filter(module=module).first()
    module_form = ModuleUpdateForm(request.POST or None, instance=module)
    dt_form = DateForm(request.POST or None, instance=instance)
    if module_form.is_valid() and dt_form.is_valid():
        module_form.save()
        dt_form.save()
        print('Saved DT!')
        if request.is_ajax():
            return dt(request, module), 'update_dt'
        else:
            return redirect('user-modules')
    context = {
        'id': module.id,
        'module_form': module_form,
        'extended_form': dt_form,
        'module_type': 'dt'
    }
    if request.is_ajax():
        form = get_template('dashboard/update_form_embedded.html')
        return form.render(context, request=request), ''
    else:
        return render(request, 'dashboard/update_form.html', context)