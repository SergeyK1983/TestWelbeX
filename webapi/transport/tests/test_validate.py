from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

from ..services import validate_zip, validate_number


class TestModels(APITestCase):

    def setUp(self):
        pass

    def test_zip_short(self):
        """ Длина меньше 5 """

        value = "0022"
        with self.assertRaises(ValidationError) as e:
            validate_zip(value)

        err = e.exception
        self.assertEqual(err.message, "0022 должно быть пять символов")

    def test_zip_only_digit(self):
        """ Должны быть только цифры """

        value = "002F2"
        with self.assertRaises(ValidationError) as e:
            validate_zip(value)

        err = e.exception
        self.assertEqual(err.message, "002F2 должно быть числом")

    def test_zip_well(self):
        """ Верный ввод """

        value = "00222"
        try:
            validate_zip(value)
        except Exception:
            self.fail("исключение возникло в validate_zip")

    def test_number_short(self):
        """ Должно быть пять символов """

        value = "0022"
        with self.assertRaises(ValidationError):
            validate_number(value)

    def test_number_last_letter(self):
        """ Последним символом должна быть буква английского алфавита"""

        value1 = "00223"
        value2 = "0022Д"
        with self.assertRaises(ValidationError):
            validate_number(value1)
        with self.assertRaises(ValidationError):
            validate_number(value2)

    def test_number_digit(self):
        """ Первые четыре символа должны быть цифры """

        value = "0F22A"
        with self.assertRaises(ValidationError):
            validate_number(value)

    def test_number_well(self):
        """ Верный ввод """

        value = "0122A"
        try:
            validate_number(value)
        except Exception:
            self.fail("исключение возникло в validate_number")

