import random

from django.utils.translation import gettext_lazy
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Location, Car, Cargo
from .services import get_cargo_all_cars, get_cargo_nearest_cars, get_cars_characteristics


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


def validate_location(location):
    """ Валидация поля ввода ZIP в CarsUpdateSerializer, CargoCreateSerializer """
    if not location.isdigit():
        raise serializers.ValidationError(gettext_lazy("Строка должна состоять из цифр."), )
    if not Location.objects.filter(zip=location).exists():
        raise serializers.ValidationError(gettext_lazy("Такого ZIP не существует, введите другой."), )
    return location


class CarsUpdateSerializer(serializers.ModelSerializer):
    """ Машины редактирование """

    cur_location = serializers.CharField(validators=[validate_location], max_length=5, min_length=5,
                                         label="Локация по ZIP")

    class Meta:
        model = Car
        fields = ["cur_location"]

    def update(self, instance, validated_data):
        zip_ = validated_data.get("cur_location")
        location = Location.objects.get(zip=zip_)
        instance.cur_location = location
        instance.save()
        return instance


class CargoCreateSerializer(serializers.ModelSerializer):
    """ Создание груза """

    loc_pick_up = serializers.CharField(validators=[validate_location], max_length=5, min_length=5,
                                        label="Локация по ZIP, пункт отправления")
    loc_delivery = serializers.CharField(validators=[validate_location], max_length=5, min_length=5,
                                         label="Локация по ZIP, пункт назначения")

    class Meta:
        model = Cargo
        fields = ["loc_pick_up", "loc_delivery", "weight", "description"]

    def validate_loc_pick_up(self, loc_pick_up):
        pick_up = self.context['request'].data.get("loc_pick_up")
        delivery = self.context['request'].data.get("loc_delivery")
        if pick_up == delivery:
            raise serializers.ValidationError(gettext_lazy(
                f"пункт отправления {pick_up} совпадает с пунктом назначения {delivery}"),
            )
        return loc_pick_up

    def create(self, validated_data):
        zip_pick_up = validated_data.pop("loc_pick_up")
        zip_delivery = validated_data.pop("loc_delivery")
        loc_pick_up = Location.objects.get(zip=zip_pick_up)
        loc_delivery = Location.objects.get(zip=zip_delivery)
        validated_data.update({"loc_pick_up": loc_pick_up})
        validated_data.update({"loc_delivery": loc_delivery})
        try:
            instance = Cargo.objects.create(**validated_data)
        except (TypeError, ValueError) as e:
            raise APIException(gettext_lazy(f"Ошибка: {type(e)} - {e}"), )
        except Exception as e:
            raise APIException(gettext_lazy(f"Ошибка: {e}"), )
        return instance


class CargoUpdateSerializer(serializers.ModelSerializer):
    """ Редактирование груза """

    class Meta:
        model = Cargo
        fields = ["weight", "description"]

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class CargoListSerializer(serializers.ModelSerializer):
    """ Информация о грузах """

    number_cars_not_more_450_miles = serializers.SerializerMethodField('get_cars')
    charact_cars = serializers.SerializerMethodField('get_characteristics_cars')

    class Meta:
        model = Cargo
        fields = ["loc_pick_up", "loc_delivery", "number_cars_not_more_450_miles", "charact_cars"]

    def get_cars(self, instance):
        cars = Car.objects.all()
        nearest_cars_count = get_cargo_nearest_cars(instance, cars)
        return nearest_cars_count

    def get_characteristics_cars(self, instance):
        cars = Car.objects.all()
        characteristics_cars = get_cars_characteristics(instance, cars)
        return characteristics_cars


class CargoSerializer(serializers.ModelSerializer):
    """ Информация о грузе """

    loc_pick_up = LocationSerializer()
    loc_delivery = LocationSerializer()
    all_cars = serializers.SerializerMethodField('get_cars')

    class Meta:
        model = Cargo
        fields = ["loc_pick_up", "loc_delivery", "weight", "description", "all_cars"]

    def get_cars(self, instance):
        cars = Car.objects.all()
        all_cars = get_cargo_all_cars(instance, cars)
        return all_cars

