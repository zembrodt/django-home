from django import forms
from .models import Image, Photos

class PhotosForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['is_background', 'width', 'height']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=1)