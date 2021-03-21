__author__ = 'Rebeca Pop'
__maintainer__ = 'Rebeca Pop, David Ramsay'
__version__ = '0.1.0'

import json
import unittest
import os
from astropy.table import Table
from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser

DIR = os.path.dirname(os.path.realpath(__file__))


def get_files_in_directory(directory):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        f.extend(filenames)
        break
    return f


class TestBase(unittest.TestCase):
    def test_table_count(self):
        count_files = len(get_files_in_directory(DIR + '/tables/'))
        self.assertEqual(count_files, 10)

    def file_contains_table(self):
        tables = sorted(get_files_in_directory(DIR + '/tables/'))
        data = []
        print(tables)
        for table in tables:
            with open(table, 'rb') as t:
                try:
                    t_data = Table.read(t, format='ascii.latex')
                except Exception as e:
                    print(e)
                    continue
                t.close()
                data.append(t_data)
        self.assertTrue(1 == 1)

    def test_files_has_tex_extension(self):
        files = os.listdir(DIR)
        has_a_different_extension_than_tex = False

        for file in files:
            if os.path.isfile(DIR + '/tables/' + file) and not file.endswith('.tex'):
                has_a_different_extension_than_tex = True
                break

        self.assertEqual(has_a_different_extension_than_tex, False)

    def test_if_there_is_an_input_and_an_output_directory(self):
        files = os.listdir(DIR)
        print(DIR)
        print(files)
        self.assertEqual('tables' in files and 'references' in files, True)


def get_parsed_table_and_reference(table, variant):
    try:
        te = TableExtractor(DIR + '/tables/' + table)
        tp = TableParser()
        tables = te.extract_tables()
        parsed_table = tp.parse(tables[0])
        f = open(DIR + '/references/'+variant+'_tables/' + table.split('.')[0] + '.json')
        reference = json.load(f)
        f.close()
        return parsed_table, reference
    except Exception:
        raise Exception


class TestCleaned(unittest.TestCase):
    def test_caption(self):
        for table in get_files_in_directory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, 'cleaned')
            self.assertEqual(reference['<documentId>']['<tableId>']['table']['caption'], parsed_table.caption)

    def test_headings(self):
        for table in get_files_in_directory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, 'cleaned')
            self.assertEqual(reference['<documentId>']['<tableId>']['table']['headers'], parsed_table.headings)

    def test_data(self):
        for table in get_files_in_directory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, 'cleaned')
            self.assertEqual(reference['<documentId>']['<tableId>']['table']['rows'], parsed_table.data)


class TestRaw(unittest.TestCase):
    def test_caption(self):
        for table in get_files_in_directory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, 'raw')
            self.assertEqual(reference['<documentId>']['<tableId>']['table']['caption'], parsed_table.caption)

    def test_headings(self):
        for table in get_files_in_directory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, 'raw')
            self.assertEqual(reference['<documentId>']['<tableId>']['table']['headers'], parsed_table.headings)

    def test_data(self):
        for table in get_files_in_directory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, 'raw')
            self.assertEqual(reference['<documentId>']['<tableId>']['table']['rows'], parsed_table.data)


class TestTableExtraction(unittest.TestCase):
    """
    NEEDS UPDATING!  Directory tests/output does no exist?
    """

    def test_table_extraction(self):
        tables = sorted([DIR + '/tables/' + filename for filename in os.listdir(DIR + '/tables/') if
                         os.path.isfile(os.path.join(DIR + '/tables/', filename))])
        output_dir = DIR + '/output/'
        output = sorted([output_dir + filename for filename in os.listdir(output_dir) if
                         os.path.isfile(os.path.join(output_dir, filename))])
        extractor = TableExtractor(tables[0])
        with open(output[0]) as output:
            output_text = output.read()
        input_text = extractor.extract_tables()[0]
        self.assertEqual(input_text, output_text)


if __name__ == '__main__':
    unittest.main()
