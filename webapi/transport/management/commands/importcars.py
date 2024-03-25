import logging
import random
import re
import rstr
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from transport.models import Location, Car

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # Возможно это стоило сделать через миграции
    help = "Загрузка в БД 20 (двадцати) случайных машин"

    def handle(self, *args, **options):
        location = Location.objects.all()
        example = re.compile(r"^[0-9]{4}[A-Z]$")
        quantity = range(20)
        blank_car = []
        if location:
            for i in quantity:
                d_car = {
                    "number": rstr.xeger(example),
                    "cur_location": random.choice(location),
                    "capacity": random.randint(1, 1000)
                }
                blank_car.append(d_car)

            list_car = [Car(**blank_car[i]) for i in quantity]

            try:
                Car.objects.bulk_create(list_car)
            except IntegrityError as e:
                logger.error(f"Во время создания машин возникли ошибки, данные не добавлены: {e}")
            except Exception as e:
                logger.error(f"Возникла непредвиденная ошибка, данные машин не добавлены: {e}")

            logger.info("Создание машин прошло успешно")
        else:
            logger.error(f"Добавить данные невозможно, список локаций пуст")

