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


class CarsCreateSerializer(serializers.ModelSerializer):
    """ Машины создание """

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
        except (TypeError, ValueError) as e:
            raise APIException(gettext_lazy(f"Ошибка: {type(e)} - {e}"), )
        except Exception as e:
            raise APIException(gettext_lazy(f"Ошибка: {e}"), )
        return instance


class CarsUpdateSerializer(serializers.ModelSerializer):
    """ Машины редактирование """

    cur_location = serializers.CharField(max_length=5, min_length=5, label="Локация по ZIP")
    # Оставлять закомментированный код нельзя! Можно было бы использовать ChoiceField, но список получился бы огромным.
    # location = serializers.ChoiceField(
    #     choices=[var.get("zip") for var in list(Location.objects.all().values("zip"))]
    # )

    class Meta:
        model = Car
        fields = ["cur_location"]

    def validate_cur_location(self, location):
        if not location.isdigit():
            raise serializers.ValidationError(gettext_lazy("Строка должна состоять из цифр."), )
        if not Location.objects.filter(zip=location).exists():
            raise serializers.ValidationError(gettext_lazy("Такого ZIP не существует, введите другой."), )
        return location

    def update(self, instance, validated_data):
        zip_ = validated_data.get("cur_location")
        location = Location.objects.get(zip=zip_)
        instance.cur_location = location
        instance.save()
        return instance



