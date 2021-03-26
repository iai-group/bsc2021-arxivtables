import os
import unittest
from arxivtables.table_extractor.table_extractor import TableExtractor

DIR = os.path.dirname(os.path.realpath(__file__))


class TestTableExtraction(unittest.TestCase):
    """
    NEEDS UPDATING!  Directory tests/output does not exist?
    """

    def test_table_extraction(self):
        tables = sorted([DIR + '/tables/' + filename for filename in os.listdir(DIR + '/tables/') if
                         os.path.isfile(os.path.join(DIR + '/tables/', filename))])
        output_dir = DIR + '/references/output/'
        output = sorted([output_dir + filename for filename in os.listdir(output_dir) if
                         os.path.isfile(os.path.join(output_dir, filename))])
        extractor = TableExtractor(tables[0])
        with open(output[0]) as output:
            output_text = output.read()
        input_text = extractor.extract_tables()[0]
        self.assertEqual(input_text, output_text)
