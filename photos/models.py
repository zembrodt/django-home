from django.db import models
from dashboard.models import Module

class Photos(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    
    # NOTE: this will need to be modified in the future to allow multiple photos per photos module
    image = models.ImageField(default='default_bg.jpg', upload_to='background_pics')

    def __str__(self):
        return f'Photos module: {self.module}'

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