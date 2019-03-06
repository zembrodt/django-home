from django import forms
from .models import Forecast
from weather.forms import UNIT_CHOICES

class ForecastForm(forms.ModelForm):
    unit = forms.ChoiceField(choices=UNIT_CHOICES)
    class Meta:
        model = Forecast
        fields = ['length', 'unit']