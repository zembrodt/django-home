from django import forms
from .models import Datetime

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