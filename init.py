import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'forex'))

import os
import csv
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forex.settings")

import django
django.setup()

from rates.models import Currency, Rate

with open('countries.txt') as f:

    reader = csv.DictReader(f, skipinitialspace=True)

    for row in reader:

        pprint.pprint(row)
        c = Currency(**row)
        c.save()
        
