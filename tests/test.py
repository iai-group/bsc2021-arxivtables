import unittest
import os
import os.path
import astropy
from astropy.table import Table


class TestStringMethods(unittest.TestCase):
    DIR = os.getcwd()+'/tests/tables/'

    def test_true(self):
        self.assertEqual(True, True)

    def test_table_count(self):
        countFiles = len([filename for filename in os.listdir(
            self.DIR) if os.path.isfile(os.path.join(self.DIR, filename))])
        self.assertEqual(countFiles, 5)

    def test_file_contains_table(self):
        tables = sorted([self.DIR + filename for filename in os.listdir(
            self.DIR) if os.path.isfile(os.path.join(self.DIR, filename))])
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

        self.assertTrue(len(data[0]) > 5)
        self.assertTrue(len(data[1]) > 5)
        self.assertTrue(len(data[2]) > 5)
        self.assertTrue(len(data[3]) > 5)
        self.assertTrue(len(data[4]) > 5)


if __name__ == '__main__':
    unittest.main()
