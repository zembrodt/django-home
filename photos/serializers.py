from rest_framework import serializers
from .models import Photos

class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ('is_background', 'width', 'height')