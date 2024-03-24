import random

from django.utils.translation import gettext_lazy
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Location, Car


class LocationSerializer(serializers.ModelSerializer):
    """ Локации """

    class Meta:
        model = Location
        fields = ["zip", "lat", "long", "state", "city"]


class CarsListSerializer(serializers.ModelSerializer):
    """ Машины просмотр """

    class Meta:
        model = Car
        fields = ["id", "number", "cur_location", "capacity"]


class CarsEditSerializer(serializers.ModelSerializer):
    """ Машины редактирование """

    class Meta:
        model = Car
        fields = ["number", "cur_location", "capacity"]
        extra_kwargs = {
            "cur_location": {'read_only': True}
        }

    def get_location(self):
        location = Location.objects.all()
        cur_location = random.choice(location)
        return cur_location

    def create(self, validated_data):
        validated_data.update({"cur_location": self.get_location()})
        try:
            instance = Car.objects.create(**validated_data)
        except TypeError as e:
            raise APIException(gettext_lazy(f"Ошибка: TypeError - {e}"), )
        except ValueError as e:
            raise APIException(gettext_lazy(f"Ошибка: ValueError - {e}"), )
        except Exception as e:
            raise APIException(gettext_lazy(f"Ошибка: {e}"), )
        return instance

