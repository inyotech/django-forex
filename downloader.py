import sys
import io
import csv
import copy
import datetime
import pprint

import requests

class Downloader:

    rates_url = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H10&series=43572f5adbac30c0ef4bcc6ce04726bb&lastobs=&from=03/01/2015&to=04/06/2017&filetype=csv&label=include&layout=seriescolumn'

    def __init__(self):
        self.raw_rate_data = None
        pass

    def retreive_rates(self):
    
        self.raw_rate_data = requests.get(self.rates_url)

    def iterate_rates(self):

        rate_data = io.StringIO(copy.copy(self.raw_rate_data.text))
        
        h10_ids = None
        reader = csv.reader(rate_data)
        for row in reader:
            try:
                row_id = row[0].strip().lower()
                if row_id == 'unique identifier:':
                    for value in row[1:]:
                        id = value.split('/')[2]
                        print(id)
                elif row_id == 'multiplier:':
                    print('multipliers')
                elif row_id == 'time period':
                    h10_ids = tuple(row[1:])
                    break
            except Exception as e:
                pprint.pprint(e)
                
        for row in reader:

            rate_date = datetime.datetime.strptime(row.pop(0), '%Y-%m-%d').date()
            
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

    downloader.retreive_rates()
    
    for rate in downloader.iterate_rates():
        pprint.pprint(rate)

    
