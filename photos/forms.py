from django import forms
from .models import Image, Photos

class PhotosForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['is_background', 'width', 'height', 'interval']

class ImageForm(forms.ModelForm):
    '''
    public = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((True, 'Public'), (False, 'Private')),
        widget=forms.RadioSelect
    )
    '''
    class Meta:
        model = Image
        fields = ['image', 'public']

ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=1)