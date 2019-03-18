from rest_framework import serializers
from .models import Datetime

class DatetimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datetime
        fields = ('twenty_four_hours', 'timezone')

