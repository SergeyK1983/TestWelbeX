import logging
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from transport.management.import_uszips_csv import import_location
from transport.models import Location

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # Возможно это стоило сделать через миграции
    help = "Загрузка в БД содержимого из файла uszips.csv в модель Location"

    def handle(self, *args, **options):
        if Location.objects.all().count() == 0:
            list_zips = import_location()
            list_keys = ("zip", "lat", "long", "city", "state")
            location_list = [Location(**dict(zip(list_keys, zips))) for zips in list_zips]

            try:
                Location.objects.bulk_create(location_list)
            except IntegrityError:
                logger.error(f"Во время импорта возникли ошибки (IntegrityError), данные не добавлены")
            except Exception:
                logger.error(f"Возникла непредвиденная ошибка, данные локаций не добавлены")

            logger.info("Импорт данных прошел успешно")
            list_zips.clear()
        else:
            logger.info("БД уже заполнена!")
