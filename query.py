import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'forex'))

import csv
import datetime
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forex.settings")

import django
from django.db import transaction

django.setup()

from rates.models import Currency, Rate, RateRatio

currencies = Currency.objects.all()

for currency in currencies:
    pprint.pprint(currency)

rates = Rate.objects.filter(rate_date=datetime.date(2017,3,28)).order_by('currency_id')

for rate in rates:
    pprint.pprint(rate)

ratios = RateRatio.objects.\
        filter(target_currency__currency_code='USD').\
        filter(base_currency__currency_code='AUD').\
        filter(rate_ratio_date__gte=datetime.date(2017,3,20))

for ratio in ratios:
    pprint.pprint(ratio)
    pprint.pprint(ratio.target_currency)
    pprint.pprint(ratio.base_currency)

ratios = RateRatio.objects.\
        filter(base_currency__currency_code='USD').\
        filter(rate_ratio_date=datetime.date(2017,3,28))

for ratio in ratios:
    pprint.pprint(ratio)
    pprint.pprint(ratio.target_currency)
    pprint.pprint(ratio.base_currency)
