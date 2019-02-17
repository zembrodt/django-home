from django.db import models
from dashboard.models import Module

class Datetime(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    twenty_four_hours = models.BooleanField(default=True)

    def __str__(self):
        return f'Datetime module: {self.module}'