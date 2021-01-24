import unittest
import os
import os.path


class TestStringMethods(unittest.TestCase):
    def test_true(self):
        self.assertEqual(True, True)

    def test_table_count(self):
        DIR = os.getcwd()+'/tests/tables'
        countFiles = len([name for name in os.listdir(
            DIR) if os.path.isfile(os.path.join(DIR, name))])
        self.assertEqual(countFiles, 5)

    def test_file_contains_table(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
