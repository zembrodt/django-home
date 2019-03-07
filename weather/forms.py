from django import forms
from .models import Weather

UNIT_CHOICES = (
    ('fahrenheit', 'Fahrenheit'),
    ('celsius', 'Celsius'),
    ('kelvin', 'Kelvin')
)
UNIT_DISPLAY = {
    'fahrenheit': 'F',
    'celsius': 'C',
    'kelvin': 'K'
}

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
    unit = forms.ChoiceField(choices=UNIT_CHOICES)
    class Meta:
        model = Weather
        fields = ['city', 'country', 'unit']
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