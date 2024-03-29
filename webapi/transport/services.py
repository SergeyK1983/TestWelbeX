import re
from geopy import distance
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Возможно стоило разделить на два файла.


def validate_zip(value):
    """ Валидация поля zip модели Location """

    if len(value) < 5:
        raise ValidationError(
            _(f"{value} должно быть пять символов"),
            params={"value": value},
        )

    if not value.isdigit():
        raise ValidationError(
            _(f"{value} должно быть числом"),
            params={"value": value},
        )


def validate_number(value):
    """ Валидация поля number модели Car """

    if len(value) < 5:
        raise ValidationError(
            _(f"{value} должно быть пять символов"),
            params={"value": value},
        )

    letter = re.compile(r"^[a-zA-Z]$")
    if not letter.search(value[-1]):
        raise ValidationError(
            _(f"{value} должна быть буква английского алфавита"),
            params={"value": value},
        )

    if not value[:4].isdigit():
        raise ValidationError(
            _(f"{value} должны быть только цифры"),
            params={"value": value},
        )


def get_geo_cars(cars) -> list:
    """ Список определенных машин """

    geo_cars = []
    for car in cars:
        geo_car = {
            "id": car.id,
            "number": car.number,
            "lat": car.cur_location.lat,
            "long": car.cur_location.long,
            "capacity": car.capacity,
        }
        geo_cars.append(geo_car)
    return geo_cars


def get_cargo_all_cars(instance, cars) -> list:
    """
    Список номеров ВСЕХ машин с расстоянием до выбранного груза.
    Используется в CargoSerializer
    """
    # в distance передавать пару кортежей (lat, lon)
    pick_up = (instance.loc_pick_up.lat, instance.loc_pick_up.long)

    # Возможно создание списка geo_cars снижает производительность и стоило использовать один цикл
    geo_cars = get_geo_cars(cars)
    all_cars = []
    for car in geo_cars:
        location_car = (car["lat"], car["long"])
        dist = round(distance.distance(pick_up, location_car).miles, 2)
        number = car["number"]
        d_car = {
            "distance_miles": dist,
            "number": number
        }
        all_cars.append(d_car)

    geo_cars.clear()
    return all_cars


def get_cargo_nearest_cars(instance, cars) -> int:
    """
    Количество ближайших машин до груза (=< 450 миль). Учтена грузоподъемность машины.
    Используется в CargoListSerializer.
    """
    pick_up = (instance.loc_pick_up.lat, instance.loc_pick_up.long)
    geo_cars = get_geo_cars(cars)
    cars = 0
    for car in geo_cars:
        location_car = (car["lat"], car["long"])
        if distance.distance(pick_up, location_car).miles <= 450:
            if car["capacity"] > instance.weight:
                cars += 1

    geo_cars.clear()
    return cars


def get_cars_characteristics(instance, cars):
    """ Характеристики ближайших к грузу машин. Используется в CargoListSerializer. """

    pick_up = (instance.loc_pick_up.lat, instance.loc_pick_up.long)
    geo_cars = get_geo_cars(cars)

    nearest_cars = []
    for car in geo_cars:
        location_car = (car["lat"], car["long"])
        if distance.distance(pick_up, location_car).miles <= 450:
            if car["capacity"] > instance.weight:
                dist = round(distance.distance(pick_up, location_car).miles, 2)
                number = car["number"]
                capacity = car["capacity"]
                d_car = {
                    "distance_miles": dist,
                    "capacity": capacity,
                    "number": number
                }
                nearest_cars.append(d_car)

    return nearest_cars

