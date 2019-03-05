from django.shortcuts import redirect, render
from django.template.loader import get_template
from .models import Datetime
from dashboard.forms import DateForm

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
    form = DateForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('user-modules')
    context = {
        'module_form': form,
        'module_type': 'dt'
    }
    return render(request, 'dashboard/update_form.html', context)