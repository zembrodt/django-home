from django.shortcuts import redirect, render
from django.template.loader import get_template
from .forms import PhotosForm
from .models import Photos, Image

def photos(request, module):
    template = get_template('photos/photos.html')
    photo = Photos.objects.filter(module=module).first()
    # temp
    images = Image.objects.filter(photos_module=photo)
    image = Image.objects.filter(photos_module=photo).first()
    
    context = {
        'photo': photo,
        'images': images,
        'count': len(images),
        'is_background': 1 if photo.is_background else 0
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
        'module_type': 'photos'
    }
    return render(request, 'dashboard/update_form.html', context)