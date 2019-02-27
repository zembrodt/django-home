from django.shortcuts import redirect, render
from django.template.loader import get_template
#from dashboard.models import Module
from .models import Photos
from dashboard.forms import PhotosForm

def photos(request, module):
    print(f'photos, module: {module}')
    template = get_template('photos/photos.html')
    photo = Photos.objects.filter(module=module).first()
    print(f'photos, photo: {photo}')
    context = {
        'photo': photo
    }
    return template.render(context)

def update_photos(request, module):
    instance = Photos.objects.filter(module=module).first()
    form = PhotosForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('user-modules')
    context = {
        'module_form': form,
        'module_type': 'Photos'
    }
    return render(request, 'dashboard/update_form.html', context)