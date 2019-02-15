from django.db import models
#from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse

class ModuleType(models.Model):
    module_type = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.module_type} ModuleType'

class Module(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    module_type = models.ForeignKey(ModuleType, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f'Module of {self.module_type} at ({self.x}, {self.y})'

    def get_absolute_url(self):
        return reverse('dashboard-home')#, kwargs={'pk': self.pk})