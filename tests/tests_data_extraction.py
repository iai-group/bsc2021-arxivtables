__author__ = "Rebeca Pop"
__maintainer__ = "Rebeca Pop, David Ramsay"

import os
import json
import unittest
from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser

DIR = os.path.dirname(os.path.realpath(__file__))


def get_file_in_directory(directory):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        f.extend(filenames)
        break
    return f


def get_parsed_table_and_reference(table, variant):
    with open(DIR + '/tables/' + table, encoding="utf8") as f:
        table_data = f.read()

    tp = TableParser()
    parsed_table = tp.parse(table_data, variant == "raw")

    with open(
            DIR + '/references/' + variant + '_tables/' +
            table.split('.')[0] + '.json', encoding="utf8"
            ) as f:
        reference = json.load(f)

    return parsed_table, reference


class TestCleaned(unittest.TestCase):
    def test_caption(self):
        for table in get_file_in_directory(DIR + '/tables/'):
            parsed_table, reference = \
                get_parsed_table_and_reference(table, "cleaned")

            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["caption"], parsed_table.caption
                )

    def test_headings(self):
        for table in get_file_in_directory(DIR + '/tables/'):
            parsed_table, reference = \
                get_parsed_table_and_reference(table, "cleaned")
            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["headers"], parsed_table.headings
                )

    def test_data(self):
        for table in get_file_in_directory(DIR + '/tables/'):
            parsed_table, reference = \
                get_parsed_table_and_reference(table, "cleaned")
            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["rows"], parsed_table.data
                )


class TestRaw(unittest.TestCase):
    def test_caption(self):
        for table in get_file_in_directory(DIR + '/tables/'):
            parsed_table, reference = \
                get_parsed_table_and_reference(table, "raw")
            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["caption"], parsed_table.caption
                )

    def test_headings(self):
        for table in get_file_in_directory(DIR + '/tables/'):
            parsed_table, reference = \
                get_parsed_table_and_reference(table, "raw")
            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["headers"], parsed_table.headings
                )

    def test_data(self):
        for table in get_file_in_directory(DIR + '/tables/'):
            parsed_table, reference = \
                get_parsed_table_and_reference(table, "raw")
            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["rows"], parsed_table.data
                )


class TestMulticolumn(unittest.TestCase):
    def test_caption(self):
        for table in get_file_in_directory(DIR + '/tables/multicolumn/'):
            parsed_table, reference = \
                get_parsed_table_and_reference('multicolumn/' + table,
                                               "multicolumn")
            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["caption"], parsed_table.caption
            )

    def test_headings(self):
        for table in get_file_in_directory(DIR + '/tables/multicolumn/'):
            parsed_table, reference = \
                get_parsed_table_and_reference('multicolumn/' + table,
                                               "multicolumn")
            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["headers"], parsed_table.headings
            )

    def test_data(self):
        for table in get_file_in_directory(DIR + '/tables/multicolumn/'):
            parsed_table, reference = \
                get_parsed_table_and_reference('multicolumn/' + table, \
                                                            "multicolumn")
            print(parsed_table)
            print(reference)
            self.assertEqual(
                reference["<documentId>"]["<tableId>"]["table"]
                ["rows"], parsed_table.data
            )
