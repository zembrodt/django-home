from django.contrib import admin
from .models import Module, ModuleType

admin.site.register(ModuleType)
admin.site.register(Module)