from django.db import models
from dashboard.models import Module

class Traffic(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return f'Traffic module: {self.module}'