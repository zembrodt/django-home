from django.db import models
from dashboard.models import Module

class Forecast(models.Model):
    module = models.OneToOneField(Module, related_name='forecast', on_delete=models.CASCADE)
    length = models.IntegerField(default=4)
    unit = models.CharField(max_length=50, default='fahrenheit')
    current_location = models.BooleanField(default=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'Forecast (module={self.module})'