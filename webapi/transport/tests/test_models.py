from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

from ..models import Location, Car, Cargo


class TestModels(APITestCase):

    def setUp(self):
        zip_ = "00235"
        lat = 63.53321
        long = -124.47851
        state = "new-state"
        city = "new-city"

        number = "5594a"
        capacity = 200

        weight = 150
        description = "Какой-то особый груз"

        Location.objects.create(zip=zip_, lat=lat, long=long, state=state, city=city)
        self.location = Location.objects.all().first()

        Car.objects.create(number=number, cur_location=self.location, capacity=capacity)
        Cargo.objects.create(loc_pick_up=self.location, loc_delivery=self.location, weight=weight,
                             description=description)

    def test_Location(self):
        """ Проверка соответствия модели Location """

        self.assertEqual(self.location.city, 'new-city')
        self.assertEqual(self.location.zip, '00235')

    def test_car(self):
        """ Проверка соответствия модели Car """

        car = Car.objects.get(cur_location=self.location.zip)
        self.assertEqual(car.number, "5594A")

    def test_cargo_fail(self):
        """ Проверка соответствия модели Cargo (Не верный экземпляр) """

        cargo = Cargo.objects.get(loc_pick_up=self.location.zip)

        self.assertEqual(cargo.loc_delivery, cargo.loc_pick_up)
        with self.assertRaises(ValidationError):
            cargo.clean_location()



