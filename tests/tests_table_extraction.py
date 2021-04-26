__author__ = 'Rebeca Pop'
__maintainer__ = 'Rebeca Pop, David Ramsay'

import os
import unittest
from arxivtables.table_extractor.table_extractor import TableExtractor

DIR = os.path.dirname(os.path.realpath(__file__))


class TestTableExtraction(unittest.TestCase):
    def test_table_extraction(self):
        tables = sorted([DIR + '/tables/' + filename for filename
                         in os.listdir(DIR + '/tables/') if
                         os.path.isfile(os.path.join(DIR + '/tables/',
                                                     filename))])
        output_dir = DIR + '/references/output/'
        output = sorted([output_dir + filename for filename
                         in os.listdir(output_dir) if
                         os.path.isfile(os.path.join(output_dir, filename))])
        extractor = TableExtractor(tables[0])
        with open(output[0]) as output:
            output_text = output.read()
        input_text = extractor.extract_tables()[0]
        self.assertEqual(input_text, output_text)

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



