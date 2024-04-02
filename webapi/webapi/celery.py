import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapi.settings')

app = Celery('webapi')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'change_location_cars-every-3-minutes': {
        'task': 'transport.tasks.change_location_cars',
        # 'schedule': 10.0,
        'schedule': crontab(minute='*/3'),  # каждые три минуты
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

