import sys
sys.path.append("/Users/scottb/PycharmProjects/forex/forex")

import os
import csv
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forex.settings")

import django
django.setup()

from rates.models import Currency, Rate

with open('countries.txt') as f:

    reader = csv.DictReader(f)

    for row in reader:

        pprint.pprint(row)
        c = Currency(**row)
        c.save()
        
#currencies = Currency.objects.all()

#pprint.pprint(currencies)
