from django.shortcuts import render
from django.template.loader import get_template

# NOTE: placeholder
def dt(request, module):
    template = get_template('dt/dt.html')
    context = {
        'id': module.id
    }
    return template.render(context)