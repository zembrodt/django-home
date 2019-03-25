from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import JsonResponse
from django.template.loader import get_template
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .forms import PhotosForm
from .models import Photos, Image
from dashboard.forms import ModuleUpdateForm
from dashboard.models import Module

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_images(request, **kwargs):
    module = get_object_or_404(Module, id=kwargs['pk'])
    photos = Photos.objects.get(module=module)
    images = Image.objects.filter(photos_module=photos)
    return JsonResponse({'images': [image.image.url for image in images]})

def photos(request, module):
    template = get_template('photos/photos.html')
    photo = Photos.objects.filter(module=module).first()
    # temp
    images = Image.objects.filter(photos_module=photo)
    
    context = {
        'photo': photo,
        'images': images,
        'count': len(images),
        'is_background': 1 if photo.is_background else 0
    }
    return template.render(context)

def update_photos(request, module):
    instance = Photos.objects.filter(module=module).first()
    module_form = ModuleUpdateForm(request.POST or None, instance=module)
    photos_form = PhotosForm(request.POST or None, instance=instance)
    if module_form.is_valid() and photos_form.is_valid():
        module_form.save()
        photos_form.save()
        if request.is_ajax():
            return photos(request, module), 'update_photos'
        else:
            return redirect('user-modules')
    context = {
        'id': module.id,
        'module_form': module_form,
        'extended_form': photos_form,
        'module_type': 'photos'
    }
    if request.is_ajax():
        form = get_template('dashboard/update_form_embedded.html')
        return form.render(context, request=request), ''
    else:
        return render(request, 'dashboard/update_form.html', context)