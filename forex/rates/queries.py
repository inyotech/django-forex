import copy

from django.db import connection

def execute_query(sql, query_params):

        result = None
        with connection.cursor() as cursor:
            cursor.execute(sql, query_params)
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return result

class RawPaginatorAdaptor:

    def __init__(self, sql, query_params=None):

        self.sql = sql
        self.query_params = query_params or []

    def count(self):

        sql_for_count = 'select count(*) n from ( %s )' % self.sql

        result = execute_query(sql_for_count, self.query_params)

        return result[0]['n']

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

        return self.execute(start=key, end=key+1)

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
