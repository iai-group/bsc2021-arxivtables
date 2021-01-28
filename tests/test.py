import unittest
import os
import os.path
import astropy
from astropy.table import Table


class TestStringMethods(unittest.TestCase):
    DIR = os.getcwd()+'/tables/'

    def test_true(self):
        self.assertEqual(True, True)

    def test_table_count(self):
        countFiles = len([filename for filename in os.listdir(
            self.DIR) if os.path.isfile(os.path.join(self.DIR, filename))])
        self.assertEqual(countFiles, 10)


    def file_contains_table(self):
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



    def test_files_has_tex_extension(self):
        files = os.listdir(self.DIR)
        hasADifferentExtensionThanTex = False

        for file in files:
            if not file.endswith('.tex'):
                hasADifferentExtensionThanTex = True
                break

        self.assertEqual(hasADifferentExtensionThanTex, False)
        

    def test_check_if_every_table_has_a_begin_table_instruction(self):
        files = os.listdir(self.DIR)

        ok = True

        for file in files:
            hasBeginTable = True

            with open(self.DIR + file, 'rb') as f:
                try:
                    content = f.read()

                    if 'begin{table' not in content.decode("utf-8"):
                        hasBeginTable = False

                        
                    f.close()
                except Exception as e:
                    print(e)
                    f.close()

            if not hasBeginTable:
                ok = False
                break
        
        self.assertEqual(ok, True)






if __name__ == '__main__':
    unittest.main()
