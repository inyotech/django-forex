import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'forex'))

import datetime
import csv
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forex.settings")

import django
from django.core import management
from django.db import transaction

django.setup()

from rates.models import Currency, Rate

def initialize_currencies():

    with open('currencies.txt') as f:

        reader = csv.DictReader(f, skipinitialspace=True)

        with transaction.atomic():

            for row in reader:
                print('Adding currency record for %(country_name)s' % row)
                c = Currency(**row)
                c.save()


management.call_command('migrate')

initialize_currencies()

start_date = datetime.datetime.now().date() - datetime.timedelta(days=5*365)

management.call_command('loadrates', start_date=start_date)

management.call_command('loadstories')
