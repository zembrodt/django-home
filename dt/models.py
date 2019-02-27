from django.db import models
from dashboard.models import Module

class Datetime(models.Model):
    module = models.ForeignKey(Module, related_name='datetimes', on_delete=models.CASCADE)
    twenty_four_hours = models.BooleanField(default=True)
    current_location = models.BooleanField(default=True)
    timezone = models.IntegerField(null=True)

    def __str__(self):
        return f'Datetime module: {self.module}'