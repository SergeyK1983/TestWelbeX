import logging
import random
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from transport.models import Location, Cargo

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # Возможно это стоило сделать через миграции
    help = "Загрузка в БД 5000 (пяти тысяч) случайных грузов для перевозки"

    def handle(self, *args, **options):
        location = Location.objects.all()
        quantity = range(5000)
        blank_cargo = []
        var = 0
        if location:
            for i in quantity:
                var += 1
                loc_pick_up = random.choice(location)
                while True:
                    loc_delivery = random.choice(location)
                    if loc_pick_up != loc_delivery:
                        break

                d_cargo = {
                    "loc_pick_up": loc_pick_up,
                    "loc_delivery": loc_delivery,
                    "weight": random.randint(1, 1000),
                    "description": f"Описание груза {var}"
                }
                blank_cargo.append(d_cargo)

            list_cargo = [Cargo(**blank_cargo[i]) for i in quantity]

            try:
                Cargo.objects.bulk_create(list_cargo)
            except IntegrityError as e:
                logger.error(f"Во время создания грузов возникли ошибки, данные не добавлены: {e}")
            except Exception as e:
                logger.error(f"Возникла непредвиденная ошибка, данные грузов не добавлены: {e}")

            logger.info("Создание грузов для перевозки прошло успешно")
        else:
            logger.error(f"Добавить данные невозможно, список локаций пуст")

