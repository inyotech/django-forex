import sys
sys.path.append("/Users/scottb/PycharmProjects/forex/forex")

import os
import csv
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forex.settings")

import django
from django.db import transaction

django.setup()

from rates.models import Currency, Rate

import downloader

all_currencies = Currency.objects.all()

pprint.pprint(all_currencies)

currency_map = {}

for currency in all_currencies:
    currency_map[currency.h10_id] = currency

pprint.pprint(currency_map)

downloader = downloader.Downloader()

downloader.retreive_rates()

with transaction.atomic():

    for rate in downloader.iterate_rates():

        pprint.pprint(rate)
        
        currency = currency_map[rate['h10_id']]
        
        pprint.pprint(currency)

        Rate.objects.update_or_create({'per_dollar': rate['per_dollar']}, currency=currency, rate_date=rate['rate_date'])
