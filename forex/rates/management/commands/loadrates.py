import datetime
import pprint

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from rates.models import Currency, Rate

import rates.rate_downloader as rate_downloader

class Command(BaseCommand):
    help = 'Downloads exchange rates and stores them in the database'

    @staticmethod
    def date_arg(string):
            return datetime.datetime.strptime(string, '%Y-%m-%d').date()

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start-date', type=Command.date_arg)
        parser.add_argument('-e', '--end-date', default=None, type=Command.date_arg)


    def handle(self, *args, **options):

        if not options['end_date']:
            options['end_date'] = datetime.datetime.now().date()

        if not options['start_date']:
            options['start_date'] = options['end_date'] - datetime.timedelta(days=10)

        pprint.pprint(options)

        all_currencies = Currency.objects.all()

        pprint.pprint(all_currencies)

        currency_map = {}

        for currency in all_currencies:
            currency_map[currency.h10_id] = currency

        pprint.pprint(currency_map)

        downloader = rate_downloader.Downloader(start_date=options['start_date'], end_date=options['end_date'])

        pprint.pprint(downloader)

        with transaction.atomic():
            for rate in downloader.iterate_rates():
                pprint.pprint(rate)
                currency = currency_map[rate['h10_id']]
                pprint.pprint(currency)
                Rate.objects.update_or_create({'per_dollar': rate['per_dollar']}, currency=currency, rate_date=rate['rate_date'])
