from rest_framework.test import APITestCase

from ..models import Location


class TestModels(APITestCase):

    def setUp(self):
        self.zip_ = "00235"
        self.lat = 63.53321
        self.long = -124.47851
        self.state = "new-state"
        self.city = "new-city"

        Location.objects.create(zip=self.zip_, lat=self.lat, long=self.long, state=self.state, city=self.city)

    def test_zip_name_label(self):
        """ Проверка соответствия наименования поля (zip) """

        location = Location.objects.get(id=1)
        field_label = location._meta.get_field('zip').verbose_name
        self.assertEqual(field_label, 'zip')



