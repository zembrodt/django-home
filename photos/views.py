from django.shortcuts import render
from django.template.loader import get_template
#from dashboard.models import Module
from .models import Photos

def photos(request, module):
    print(f'photos, module: {module}')
    template = get_template('photos/photos.html')
    photo = Photos.objects.filter(module=module).first()
    print(f'photos, photo: {photo}')
    context = {
        'photo': photo
    }
    return template.render(context)