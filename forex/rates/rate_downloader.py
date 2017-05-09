import io
import csv
import copy
import datetime
import pprint

import requests

class Downloader:

    rates_url = ('https://www.federalreserve.gov/datadownload/Output.aspx'
                 '?rel=H10&series=43572f5adbac30c0ef4bcc6ce04726bb&lastobs=&'
                 'from=%(start)s&to=%(end)s'
                 '&filetype=csv&label=include&layout=seriescolumn')

    def __init__(self,  start_date=None, end_date=None):

        if not end_date:
            self.end_date = datetime.datetime.now().date()
        else:
            self.end_date = end_date

        if not start_date:
            self.start_date = self.end_date - datetime.timedelta(days=10)
        else:
            self.start_date = start_date

    def iterate_rates(self):

        url = self.rates_url % {'start': self.start_date, 'end': self.end_date}
        raw_rate_data = requests.get(url)

        raw_rate_data.raise_for_status()

        print('Retrieved exchange rates from %s' % (url,))

        rate_data = io.StringIO(copy.copy(raw_rate_data.text))

        h10_ids = None
        reader = csv.reader(rate_data)
        for row in reader:
            try:
                row_id = row[0].strip().lower()
                if row_id == 'unique identifier:':
                    for value in row[1:]:
                        id = value.split('/')[2]
                elif row_id == 'multiplier:':
                    pass
                elif row_id == 'time period':
                    h10_ids = tuple(row[1:])
                    break
            except Exception as e:
                pprint.pprint(e)

        for row in reader:

            rate_date = datetime.datetime.strptime(row.pop(0), '%Y-%m-%d').date()

            print('Adding rates for %s' % (rate_date,))

            r = {
                'h10_id': 'RXI_N.B.US',
                'rate_date': rate_date,
                'per_dollar': 1.0,
            }
            yield r

            row = dict(zip(h10_ids, row))

            for h10_id, per_dollar in row.items():
                if per_dollar == 'ND':
                    continue
                elif h10_id.startswith('RXI$US_N'):
                    per_dollar = 1.0/float(per_dollar)
                    h10_id = h10_id.replace('$US', '')
                else:
                    per_dollar = float(per_dollar)

                r = {
                    'h10_id': h10_id,
                    'rate_date': rate_date,
                    'per_dollar': per_dollar,
                }

                yield r

if __name__ == '__main__':

    downloader = Downloader()

    for rate in downloader.iterate_rates():
        pprint.pprint(rate)
