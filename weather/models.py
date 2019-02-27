from django.db import models
from dashboard.models import Module

class Weather(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    current_location = models.BooleanField(default=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    show_forecast = models.BooleanField()
    forecast_length = models.IntegerField(default=4)

    def __str__(self):
        return f'Weather module: {self.module}'