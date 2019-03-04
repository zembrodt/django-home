from django.db import models
from django.contrib.auth.models import User
#from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    slogan = models.CharField(max_length=50)
    #image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    #modules = models.ManyToManyField(Module)

    def __str__(self):
        return f'{self.user.username} Profile'

    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    """