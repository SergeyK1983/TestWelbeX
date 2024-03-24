from django.core.exceptions import ValidationError
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .services import validate_zip, validate_number


class Car(models.Model):
    """ Машина для перевозок """

    number = models.CharField(validators=[validate_number], max_length=5, unique=True, verbose_name="Машина",
                              help_text="Например: 7952D или 5621a")
    cur_location = models.ForeignKey(to='Location', to_field="zip", related_name="cars", on_delete=models.CASCADE,
                                     verbose_name="Текущая локация")
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)],
                                   verbose_name="Грузоподъемность", help_text="от 1 до 1000")

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"
        ordering = ["id", "cur_location"]

    def save(self, *args, **kwargs):
        self.number = self.number.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: {self.number} in {self.cur_location}"

    def get_update_url(self):
        return reverse(viewname="update-car", kwargs={"id": self.id})


class Location(models.Model):
    """ Локация местонахождения """

    zip = models.CharField(validators=[validate_zip, ], max_length=5, unique=True, help_text="пример: 00000")
    lat = models.DecimalField(validators=[MinValueValidator(-90.00000), MaxValueValidator(90.00000)],
                              max_digits=7, decimal_places=5, verbose_name="Широта", help_text="широта в градусах")
    long = models.DecimalField(validators=[MinValueValidator(-180.00000), MaxValueValidator(180.00000)],
                               max_digits=8, decimal_places=5, verbose_name="Долгота", help_text="долгота в градусах")

    state = models.CharField(max_length=100, verbose_name="Штат")
    city = models.CharField(max_length=100, verbose_name="Город")

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        ordering = ["zip"]

    def __str__(self):
        return f"{self.zip}: {self.state} - {self.city}"


class Cargo(models.Model):
    """ Груз """

    loc_pick_up = models.ForeignKey(to=Location, to_field="zip", related_name="pick_up", on_delete=models.CASCADE,
                                    verbose_name="Отправитель")
    loc_delivery = models.ForeignKey(to=Location, to_field="zip", related_name="delivery", on_delete=models.CASCADE,
                                     verbose_name="Назначение")
    weight = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], verbose_name="Вес",
                                 default=100, help_text="от 1 до 1000")
    description = models.TextField(max_length=2000, verbose_name="Описание", default="Описание груза",
                                   help_text="не более 2000 знаков")

    class Meta:
        verbose_name = "Груз"
        verbose_name_plural = "Грузы"
        ordering = ["id", "loc_pick_up", "loc_delivery"]

    def __str__(self):
        return f"{self.id}: {self.loc_pick_up} to {self.loc_delivery}"

    def get_absolute_url(self):
        return reverse(viewname='cargo', kwargs={'id': self.id})
