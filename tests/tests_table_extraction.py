import os
import unittest
from astropy.table import Table
from tests.tests_data_extraction import GetFilesInDirectory, DIR


class TestBase(unittest.TestCase):
    def test_table_count(self):
        countFiles = len(GetFilesInDirectory(DIR + '/tables/'))
        self.assertEqual(countFiles, 10)

    def file_contains_table(self):
        tables = sorted(GetFilesInDirectory(DIR + '/tables/'))
        data = []
        print(tables)
        for table in tables:
            tData = ' '
            with open(table, 'rb') as t:
                try:
                    tData = Table.read(t, format="ascii.latex")
                except Exception as e:
                    print(e)
                    continue
                t.close()
                data.append(tData)

    def test_files_has_tex_extension(self):
        files = os.listdir(DIR)
        hasADifferentExtensionThanTex = False

        for file in files:
            if os.path.isfile(DIR + '/tables/' + file) and not file.endswith('.tex'):
                hasADifferentExtensionThanTex = True
                break

        self.assertEqual(hasADifferentExtensionThanTex, False)

    def test_if_there_is_an_input_and_an_output_directory(self):
        files = os.listdir(DIR)
        print(DIR)
        print(files)
        self.assertEqual('tables' in files and 'references' in files, True)
