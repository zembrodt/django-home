from rest_framework import serializers
from .models import Module, ModuleType
from dt.models import Datetime
from forecast.models import Forecast
from photos.models import Photos
from users.models import Profile
from weather.models import Weather
from dt.serializers import DatetimeSerializer
from forecast.serializers import ForecastSerializer
from photos.serializers import PhotosSerializer
from weather.serializers import WeatherSerializer

class ModuleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleType
        fields = ('module_type', 'name')

class ModuleSerializer(serializers.ModelSerializer):
    #module_type = serializers.PrimaryKeyRelatedField(queryset=ModuleType.objects.all())
    submodule = serializers.SerializerMethodField()
    class Meta:
        model = Module
        depth = 1
        fields = ('id', 'module_type', 'x', 'y', 'z_index', 'text_color', 'submodule')

    def get_submodule(self, obj):
        print(f'get_submodule: obj: {obj}')
        # if not isinstance(obj, Module):
        #     obj = ModuleSerializer(obj)
        if obj.module_type.module_type == 'dt':
            return DatetimeSerializer(obj.dt).data
        elif obj.module_type.module_type == 'forecast':
            return ForecastSerializer(obj.forecast).data
        elif obj.module_type.module_type == 'photos':
            return PhotosSerializer(obj.photos).data
        elif obj.module_type.module_type == 'weather':
            return WeatherSerializer(obj.weather).data
        else:
            return None

    def create(self, validated_data):
        submodule_data = validated_data.pop('submodule')
        module_type = validated_data.pop('module_type')
        module_type_obj = ModuleType.objects.get(module_type=module_type)
        user = Profile.objects.get(user=self.context['request'].user)
        module = Module.objects.create(**validated_data, module_type=module_type_obj, owner=user)

        # TODO: We should possible create a check that the submodule_data is valid before creating the module
        
        if module_type == 'dt':
            Datetime.objects.create(**submodule_data, module=module)
        elif module_type == 'forecast':
            Forecast.objects.create(**submodule_data, module=module)
        elif module_type == 'photos':
            Photos.objects.create(**submodule_data, module=module)
        elif module_type == 'weather':
            Weather.objects.create(**submodule_data, module=module)

    def update(self, instance, validated_data):
        print(f'instance: {instance}\nvalidated data: {validated_data}')
        is_submodule = False
        if 'submodule' in validated_data:
            is_submodule = True
            submodule_data = validated_data.pop('submodule')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        #submodule = instance.submodule

        print(f'instance: {instance}\nmodule type: {instance.module_type}\ntype 2: {instance.module_type.module_type}')
        

        # Save the module
        instance.x = validated_data.get('x', instance.x)
        instance.y = validated_data.get('y', instance.y)
        instance.z_index = validated_data.get('z_index', instance.z_index)
        instance.text_color = validated_data.get('text_color', instance.text_color)
        instance.save()

        # Save the submodule
        if is_submodule:
            module_type = instance.module_type.module_type
            
            if module_type == 'dt':
                serializer = DatetimeSerializer(data=submodule_data)
                print('Got dt serializer')
                if serializer.is_valid():
                    print('dt serializer valid')
                    serializer.update(instance.dt, submodule_data)
                else:
                    print(f'dt serializer data NOT valid: {submodule_data}')
            elif module_type == 'forecast':
                serializer = ForecastSerializer(data=submodule_data)
                if serializer.is_valid():
                    serializer.update(instance.forecast, submodule_data)
            elif module_type == 'photos':
                serializer = PhotosSerializer(data=submodule_data)
                if serializer.is_valid():
                    serializer.update(instance.photos, submodule_data)
            elif module_type == 'weather':
                serializer = WeatherSerializer(data=submodule_data)
                if serializer.is_valid():
                    serializer.update(instance.weather, submodule_data)
        # profile.has_support_contract = profile_data.get(
        #     'has_support_contract',
        #     profile.has_support_contract
        #  )
        # profile.save()

        return instance