from django.test import TestCase
from django.core.paginator import Paginator, EmptyPage

from rates.queries import RawPaginatorAdaptor

class RawPaginationWrapper(RawPaginatorAdaptor):

    def __init__(self, row_count, test_executor):
        self.row_count = row_count
        self.text_executor = test_executor

    def count(self):
        return self.row_count

    def execute(self, start=0, end=None):
        return self.text_executor(start, end)

class PaginationTestCase(TestCase):

    def assert_start_end(self, expected_start, expected_end):
        def asserts(start, end):
            print("expected:seen start %d:%d end %d:%d" % (expected_start, start, expected_end, end))
            self.assertEqual(expected_start, start)
            self.assertEqual(expected_end, end)
        return asserts

    def test_pagination(self):

        adaptor = RawPaginationWrapper(row_count=50, test_executor=self.assert_start_end(expected_start=0, expected_end=10))
        paginator = Paginator(adaptor, per_page=10)

        self.assertEqual(paginator.count, 50)
        self.assertEqual(paginator.num_pages, 5)

        page = paginator.page(1)

        self.assertTrue(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertEqual(page.start_index(), 1)
        self.assertEqual(page.end_index(), 10)

        adaptor = RawPaginationWrapper(row_count=50, test_executor=self.assert_start_end(expected_start=10, expected_end=20))
        paginator = Paginator(adaptor, per_page=10)

        page = paginator.page(2)

        self.assertTrue(page.has_next())
        self.assertTrue(page.has_previous())
        self.assertEqual(page.start_index(), 11)
        self.assertEqual(page.end_index(), 20)

        adaptor = RawPaginationWrapper(row_count=5, test_executor=self.assert_start_end(expected_start=0, expected_end=5))
        paginator = Paginator(adaptor, per_page=10)

        page = paginator.page(1)

        self.assertFalse(page.has_next())
        self.assertFalse(page.has_previous())
        self.assertEqual(page.start_index(), 1)
        self.assertEqual(page.end_index(), 5)

        self.assertRaises(EmptyPage, paginator.page, 0)
        self.assertRaises(EmptyPage, paginator.page, 2)
