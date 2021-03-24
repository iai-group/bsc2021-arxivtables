__author__ = "Rebeca Pop"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

import json
import unittest
import os
from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser

DIR = os.path.dirname(os.path.realpath(__file__))


def GetFilesInDirectory(directory):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        f.extend(filenames)
        break
    return f

def get_parsed_table_and_reference(table, variant):
    try:
        te = TableExtractor(DIR + '/tables/' + table)
        tp = TableParser()
        tables = te.extract_tables()
        parsed_table = tp.parse(tables[0], variant == "raw")
        f = open(DIR + '/references/'+variant+'_tables/' + table.split('.')[0] + '.json')
        reference = json.load(f)
        f.close()
        return parsed_table, reference
    except Exception:
        raise Exception

class TestCleaned(unittest.TestCase):
    def test_caption(self):
        for table in GetFilesInDirectory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, "cleaned")
            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["caption"], parsed_table.caption)

    def test_headings(self):
        for table in GetFilesInDirectory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, "cleaned")
            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["headers"], parsed_table.headings)

    def test_data(self):
        for table in GetFilesInDirectory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, "cleaned")
            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["rows"], parsed_table.data)


class TestRaw(unittest.TestCase):
    def test_caption(self):
        for table in GetFilesInDirectory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, "raw")
            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["caption"], parsed_table.caption)

    def test_headings(self):
        for table in GetFilesInDirectory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, "raw")
            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["headers"], parsed_table.headings)

    def test_data(self):
        for table in GetFilesInDirectory(DIR + '/tables/'):
            if table == 'table_5.tex':
                continue
            parsed_table, reference = get_parsed_table_and_reference(table, "raw")
            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["rows"], parsed_table.data)


class TestTableExtraction(unittest.TestCase):
    """
    NEEDS UPDATING!  Directory tests/output does no exist?
    """

    def test_table_extraction(self):
        tables = sorted([DIR + '/tables/' + filename for filename in os.listdir(DIR + '/tables/') if
                         os.path.isfile(os.path.join(DIR + '/tables/', filename))])
        outputDIR = DIR + '/output/'
        output = sorted([outputDIR + filename for filename in os.listdir(outputDIR) if
                         os.path.isfile(os.path.join(outputDIR, filename))])
        extractor = TableExtractor(tables[0])
        with open(output[0]) as output:
            outputText = output.read()
        inputText = extractor.extract_tables()[0]
        self.assertEqual(inputText, outputText)


if __name__ == '__main__':
    unittest.main()