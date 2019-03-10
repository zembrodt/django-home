from django import forms
from django.forms.widgets import TextInput
from .models import Module

class ModuleCreateForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['module_type', 'x', 'y', 'z_index', 'text_color']
        widgets = {
            'text_color': TextInput(attrs={'type': 'color'}),
        }
        # NOTE: this is an incorrect way to do widgets
        '''
        widgets = {
            'module_type': forms.Select(attrs={
                #'class': 'blah',
                'id': 'module_type'
            })
        }
        '''

class ModuleUpdateForm(forms.ModelForm):
    class Meta:
        model = Module
        # Only want to allow users to update fields they can't otherwise update on the dashboard-update page
        fields = ['text_color']
        widgets = {
            'text_color': TextInput(attrs={'type': 'color'}),
        }