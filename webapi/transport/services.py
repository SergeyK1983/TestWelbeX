import re
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

    letter = re.compile(r"^[a-zA-Z]$")
    if letter.search(value[-1]):
        raise ValidationError(
            _(f"{value} должна быть буква английского алфавита"),
            params={"value": value},
        )

    if not value[:4].isdigit():
        raise ValidationError(
            _(f"{value} должны быть только цифры"),
            params={"value": value},
        )

