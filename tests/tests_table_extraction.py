__author__ = 'Rebeca Pop'
__maintainer__ = 'Rebeca Pop, David Ramsay'

import os
import unittest
from arxivtables.table_extractor.table_extractor import TableExtractor

DIR = os.path.dirname(os.path.realpath(__file__))


class TestTableExtraction(unittest.TestCase):
    def test_multiple_tables_extraction(self):
        paper_id = "2104.05695"

        extractor = TableExtractor(paper_id)
        extractor.extract_files()
        tables = extractor.extract_tables()

        for index in range(len(tables)):
            with open("references/extracted_tables/" + paper_id + "/" +
                      str(index) + ".tex", "r") as f:
                reference = "".join(f.readlines())
                self.assertEqual(tables[index], reference)

