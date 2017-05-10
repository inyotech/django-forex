import io
import datetime
import csv

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse

import rates.queries as queries

def historic_rates(request, base='USD', target='EUR', months=24):

    months = int(months)

    sql = ('select '
           'country_name, '
           'short_name, '
           'currency_name, '
           'currency_code '
           'from currencies where currency_code = %s ')

    target_currency = queries.execute_query(sql, [target])[0]

    base_currency = queries.execute_query(sql, [base])[0]

    sql = ('select '
           'target_rates.rate_date, '
           'target_rates.per_dollar / base_rates.per_dollar rate_ratio '
           'from exchange_rates target_rates '
           'join exchange_rates base_rates on base_rates.rate_date = target_rates.rate_date '
           "where target_rates.currency_id = (select currency_id from currencies where currency_code = %s) "
           " and base_rates.currency_id = (select currency_id from currencies where currency_code = %s) "
           " and target_rates.rate_date > %s and target_rates.rate_date <= %s "
           'order by target_rates.rate_date ')

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=months*30)
    params = [target, base, start_date, end_date]

    page = int(request.GET['page']) if 'page' in request.GET else False

    if page:
        page_length = request.GET.get('per_page', 25)
        object_list = queries.RawPaginatorAdaptor(sql, params)
        paginator = Paginator(object_list, page_length)
        data = paginator.page(page).object_list
    else:
        data = queries.execute_query(sql, params)

    response = {
        'target': target_currency,
        'base': base_currency,
        'data': data,
    }

    if request.GET.get('csv'):
        return csv_response(response)

    if page:
        response['pages'] = {
            'page': page,
            'per_page': paginator.per_page,
            'num_pages': paginator.num_pages,
        }

    return JsonResponse(response)

def csv_response(response_data):

    buffer = io.StringIO()
    writer = csv.writer(buffer, quoting=csv.QUOTE_ALL)

    writer.writerow(['base_currency_code', 'base_country_name', 'base_currency_name'])
    writer.writerow([
        response_data['base']['currency_code'],
        response_data['base']['country_name'],
        response_data['base']['currency_name'],
    ])

    writer.writerow([])

    writer.writerow(['target_currency_code', 'target_country_name', 'target_currency_name'])
    writer.writerow([
        response_data['target']['currency_code'],
        response_data['target']['country_name'],
        response_data['target']['currency_name'],
    ])

    writer.writerow([])

    writer.writerow(['date', 'exchange_rate'])
    for rate in response_data['data']:
        writer.writerow([
            rate['rate_date'],
            rate['rate_ratio'],
        ])

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exchangerates.csv"'

    return response

def current_rates(request, base='USD'):

    sql = ('select '
           'country_name, '
           'short_name, '
           'currency_name, '
           'currency_code '
           'from currencies where currency_code = %s ')

    base_currency = queries.execute_query(sql, [base])[0]

    sql = ('select '
           'target_currency.country_name, '
           'target_currency.short_name, '
           'target_currency.currency_name, '
           'target_currency.currency_code, '
           'target_currency.flag_image_file_name, '
           'target_rates.rate_date, '
           'target_rates.per_dollar / base_rates.per_dollar rate_ratio '
           'from exchange_rates target_rates '
           'join exchange_rates base_rates on base_rates.rate_date = target_rates.rate_date '
           'join currencies target_currency on target_currency.currency_id = target_rates.currency_id '
           "where base_rates.currency_id = (select currency_id from currencies where currency_code = %s) "
           ' and target_rates.rate_date = (select max(rate_date) from exchange_rates) '
           'order by target_currency.country_name ')

    data = queries.execute_query(sql, [base])

    response = {
        'base': base_currency,
        'data': data,
    }

    return JsonResponse(response)
