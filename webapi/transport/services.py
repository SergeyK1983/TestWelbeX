import re
from geopy import distance
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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


def get_cargo_all_cars(instance, cars) -> list:
    """
    Список номеров ВСЕХ машин с расстоянием до выбранного груза.
    Используется в CargoSerializer
    """
    pick_up = (instance.loc_pick_up.lat, instance.loc_pick_up.long)

    # Возможно создание списка geo_cars снижает производительность и стоило использовать один цикл
    geo_cars = []
    for car in cars:
        geo_car = {
            "id": car.id,
            "number": car.number,
            "lat": car.cur_location.lat,
            "long": car.cur_location.long
        }
        geo_cars.append(geo_car)

    all_cars = []
    for car in geo_cars:
        location_car = (car["lat"], car["long"])
        dist = round(distance.distance(pick_up, location_car).miles, 2)
        number = car["number"]
        d_car = {
            "distance": dist,
            "number": number
        }
        all_cars.append(d_car)

    geo_cars.clear()
    return all_cars
