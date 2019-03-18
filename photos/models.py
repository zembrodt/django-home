from django.db import models
from django.template.defaultfilters import slugify
from dashboard.models import Module
from users.models import Profile

class Photos(models.Model):
    module = models.OneToOneField(Module, related_name='photos', on_delete=models.CASCADE)
    is_background = models.BooleanField(default=False)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    interval = models.IntegerField(default=5)
    

    # NOTE: this will need to be modified in the future to allow multiple photos per photos module
    #image = models.ImageField(default='default_bg.jpg', upload_to='background_pics')

    def __str__(self):
        return f'Photos module: {self.module}'

def get_image_filename(instance, filename):
    #slug = slugify(filename)
    #return f'background_pics/{slug}-{filename}'
    return f'user_images/{filename}'

class Image(models.Model):
    owner = models.ForeignKey(Profile, related_name='images', on_delete=models.CASCADE)
    photos_module = models.ForeignKey(Photos, related_name='images', null=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=False, upload_to=get_image_filename)
    public = models.BooleanField(default=True)

    # Seems we only need this if we want to edit the image before saving (Max at a 1080p image? 4k?)
    '''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    '''

    def __str__(self):
        return f'Image for Photos module: {self.photos_module}'

# TODO: If a user can upload their own images separaately from a photos module, we need a mapper so multiple modules
#       can reference the same images
'''
class ImageToPhotos(models.Model):
    image = models.ForeignKey(Image, related_name='photos')
'''