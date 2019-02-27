from django.contrib import admin
from .models import Photos, Image
from .forms import PhotosForm


class ImageInLine(admin.StackedInline):
    model = Image
    extra = 0

admin.site.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    form = PhotosForm
    inlines = [ImageInLine]

    def save_model(self, request, obj, form, change):
        super(PhotosAdmin, self).save_model(request, obj, form, change)

        # photos_multiple: name of the image field
        for f in request.FILES.getlist('photos_multiple'): 
            obj.images.create(file=f)



admin.site.register(Image)