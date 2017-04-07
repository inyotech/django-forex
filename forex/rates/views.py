import copy
import datetime
import pprint

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import connection

def execute_query(sql, query_params):

        result = None
        with connection.cursor() as cursor:
            cursor.execute(sql, query_params)
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

class PaginatorObjectList:

    def __init__(self, sql, query_params=None):

        self.sql = sql
        self.query_params = query_params or []

    def count(self):

        sql_for_count = 'select count(*) from ( %s )' % self.sql

        result = None
        with connection.cursor() as cursor:
            cursor.execute(sql_for_count, self.query_params)
            result = cursor.fetchone()[0]

        return result

    def __len__(self):

        return self.count()

    def __getitem__(self, key):

        if not isinstance(key, (int, slice)):
            raise TypeError

        if isinstance(key, slice):
            if key.start is not None:
                start = int(key.start)
            else:
                start = None

            if key.stop is not None:
                stop = int(key.stop)
            else:
                stop = None

            return self.execute(start=start, end=stop)

        return self.execute(limit=key+1, offset=key)

    def execute(self, start=0, end=None):

        sql = copy.copy(self.sql)
        params = copy.copy(self.query_params)

        if end is not None:
            if start is not None:
                sql += ' limit %d ' % (end - start)
            else:
                sql += ' limit %d ' % end

        if start is not None:
            sql += ' offset %d ' % start

        return execute_query(sql, params)

def historic_rates(request, base='USD', target='EUR', months=24, page=None, per_page=10):

    sql = ('select '
           'country_name, '
           'short_name, '
           'currency_name, '
           'currency_code '
           'from currencies where currency_code = %s ')

    target_currency = execute_query(sql, [target])[0]

    base_currency = execute_query(sql, [base])[0]

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

    if page:
        object_list = PaginatorObjectList(sql, params)
        paginator = Paginator(object_list, per_page)
        data = paginator.page(page).object_list
    else:
        data = execute_query(sql, params)

    response = {
        'target': target_currency,
        'base': base_currency,
        'data': data,
    }

    if page:
        response['pages'] = {
            'page': page,
            'per_page': paginator.per_page,
            'num_pages': paginator.num_pages,
        }

    return JsonResponse(response)

def current_rates(request, base='USD'):

    sql = ('select '
           'country_name, '
           'short_name, '
           'currency_name, '
           'currency_code '
           'from currencies where currency_code = %s ')

    base_currency = execute_query(sql, [base])[0]

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

    data = execute_query(sql, [base])

    response = {
        'base': base_currency,
        'data': data,
    }

    return JsonResponse(response)
