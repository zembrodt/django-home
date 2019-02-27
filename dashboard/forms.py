from django import forms
from .models import Module
from dt.models import Datetime
from photos.models import Photos
from weather.models import Weather

class ModuleCreateForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ['module_type', 'x', 'y']
        # NOTE: this is an incorrect way to do widgets
        '''
        widgets = {
            'module_type': forms.Select(attrs={
                #'class': 'blah',
                'id': 'module_type'
            })
        }
        '''

# NOTE: forms in this file temporarily
class DateForm(forms.ModelForm):
    '''
    def __init__(self, *args, **kwargs):
        if 'module' in kwargs:
            module = kwargs.pop('module')
            super(DateForm, self).__init__(*args, **kwargs)
            self.fields['module'] = module
        else:
            super(DateForm, self).__init__(*args, **kwargs)
    '''
    class Meta:
        model = Datetime
        fields = ['twenty_four_hours']
        #widgets = {
        #    'twenty_four_hours': forms.CheckboxInput()
        #}
        
class WeatherForm(forms.ModelForm):
    '''
    def __init__(self, *args, **kwargs):
        if 'module' in kwargs:
            module = kwargs.pop('module')
            super(WeatherForm, self).__init__(*args, **kwargs)
            self.fields['module'] = module
        else:
            super(WeatherForm, self).__init__(*args, **kwargs)
    '''
    class Meta:
        model = Weather
        fields = ['show_forecast', 'forecast_length']
        '''
        widgets = {
            'show_forecast': forms.CheckboxInput(attrs={
                'id': 'show_forecast'
            }),
            'forecast_length': forms.IntegerField(attrs={
                'id': 'forecast_length'
            })
        }
        '''

class PhotosForm(forms.ModelForm):
    class Meta:
        model = Photos
        #fields = ['is_background', 'width', 'height']
        fields = ['width', 'height']