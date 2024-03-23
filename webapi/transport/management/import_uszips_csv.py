import csv
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
path_folder = os.path.join(BASE_DIR, 'locations_data')
path_file = os.path.join(path_folder, 'uszips.csv')


def import_location():
    list_zips = []

    with open(path_file, mode='r', encoding='utf8') as zips:
        # показалось, что в данном случае со csv.DictReader возни будет больше
        var = -1
        reader = csv.reader(zips)
        for row in reader:
            var += 1
            if var == 0:
                continue

            line = row[:6]
            line.pop(4)
            list_zips.append(line)

            if var == 1000:
                break

    return list_zips
