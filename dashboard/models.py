from django.db import models

class Module(models.Model):
    module_type = models.CharField(max_length=50)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f'Module of {self.module_type} at ({self.x}, {self.y})'