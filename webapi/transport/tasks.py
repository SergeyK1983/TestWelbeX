import os
import random
from pathlib import Path
from datetime import datetime
from webapi.celery import app

from .models import Car, Location


BASE_DIR = Path(__file__).resolve().parent.parent
FILE = os.path.join(BASE_DIR, 'log-celery.txt')


@app.task
def change_location_cars():
    location = Location.objects.all()
    cars = Car.objects.all()
    c = []
    for car in cars:
        car.cur_location = random.choice(location)
        c.append(car)

    Car.objects.bulk_update(c, ["cur_location"])
    c.clear()

    with open(FILE, mode='a', encoding='utf8') as log:
        log.write(f"Локации машин изменены {datetime.now()}\n")

    return
