import random

from django.utils.translation import gettext_lazy
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .filters import CapacityCarsFilter, DistanceCarsFilter
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


class CarsSerializer(serializers.ModelSerializer):
    """ Машины """

    distance_miles = serializers.SerializerMethodField('get_dist')

    class Meta:
        model = Car
        fields = ["distance_miles", "number", "cur_location", "capacity"]

    def get_dist(self, instance):
        cargo = self.context['cargo']
        dist = instance.get_dist_to_cargo(cargo)
        return dist


class CargoListSerializer(serializers.ModelSerializer):
    """ Информация о грузах """

    number_cars_not_more_450_miles = serializers.SerializerMethodField('get_cars')
    charact_cars = serializers.SerializerMethodField('get_characteristics_cars')

    class Meta:
        model = Cargo
        fields = ["loc_pick_up", "loc_delivery", "weight", "number_cars_not_more_450_miles", "charact_cars"]

    def get_cars(self, instance):
        # print("ser:  ", self.context['request'].GET)
        cars = Car.objects.all()
        nearest_cars_count = get_cargo_nearest_cars(instance, cars)
        return nearest_cars_count

    def get_characteristics_cars(self, instance):
        request = self.context['request'].GET
        cap_gte = request.get('cap_gte', None)
        cap_lte = request.get('cap_lte', None)
        dist_gte = request.get('dist_gte', None)
        dist_lte = request.get('dist_lte', None)

        cars = Car.objects.all()
        # f_cars = CarsCapacityFilter(queryset=cars, request=self.context['request'])
        characteristics_cars = get_cars_characteristics(instance, cars)
        ser = CarsSerializer(instance=instance.get_nearest_cars(), many=True, context={'cargo': instance})

        filter_cap = CapacityCarsFilter(ser.data, cap_gte, cap_lte)  # фильтрация по грузоподъемности
        ser_filtering_cap = filter_cap.get_filter_capacity_cars()  # фильтр по грузоподъемности

        filter_dist = DistanceCarsFilter(ser_filtering_cap, dist_gte, dist_lte)  # фильтрация по дальности до груза
        ser_filtering_dist = filter_dist.get_filter_distance_cars()  # фильтр по дальности

        return ser_filtering_dist
        # return characteristics_cars


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

