import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = "admin"
            email = "mail@mail.ru"
            password = "admin"
            logger.info(f"Создан админ {username}, email {email}, password {password}")
            User.objects.create_superuser(email=email, username=username, password=password)
        else:
            logger.info('Админ не создался')

