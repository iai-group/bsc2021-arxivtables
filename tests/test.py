__author__ = "Rebeca Pop"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

import json
import unittest
import os
import os.path
from tex2py import tex2py
from astropy.table import Table
from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser


DIR = os.path.dirname(os.path.realpath(__file__))

class TestBase(unittest.TestCase):
    def test_table_count(self):
        countFiles = len([filename for filename in os.listdir(
            DIR+'/tables/') if os.path.isfile(os.path.join(DIR+'/tables/', filename))])
        self.assertEqual(countFiles, 10)

    def file_contains_table(self):
        tables = sorted([DIR+'/tables/' + filename for filename in os.listdir(
            DIR+'/tables/') if os.path.isfile(os.path.join(DIR+'/tables/', filename))])
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
            if os.path.isfile(DIR+'/tables/' + file) and not file.endswith('.tex'):
                hasADifferentExtensionThanTex = True
                break

        self.assertEqual(hasADifferentExtensionThanTex, False)

    def test_check_if_every_table_has_a_begin_table_instruction(self):
        files = os.listdir(DIR+'/tables/')

        ok = True

        for file in files:
            if os.path.isdir(DIR+'/tables/' + file):
                continue

            hasBeginTable = True

            with open(DIR+'/tables/' + file, 'rb') as f:
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

    
    def test_if_there_is_an_input_and_an_output_directory(self):
        files = os.listdir(DIR)
        print(DIR)
        print(files)
        self.assertEqual("tables" in files and "references" in files, True)


class TestCleaned(unittest.TestCase):
    def test_caption(self):
        for table_index in range(1, 10):
            te = TableExtractor(DIR+"/tables/table_" + str(table_index) + ".tex")
            tp = TableParser()

            tables = te.extract_tables()
            if not tables:
                continue
            #self.assertTrue(len(tables) > 0)
            parsed_table = tp.parse(tables[0])

            f = open(DIR+"/references/cleaned_tables/table_" + str(table_index) + ".json")
            reference = json.load(f)
            f.close()

            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["caption"], parsed_table.caption)

    def test_headings(self):
        for table_index in range(1, 10):
            te = TableExtractor(DIR+"/tables/table_" + str(table_index) + ".tex")
            tp = TableParser()

            tables = te.extract_tables()
            if not tables:
                continue
            #self.assertTrue(len(tables) > 0)
            parsed_table = tp.parse(tables[0])

            f = open(DIR+"/references/cleaned_tables/table_" + str(table_index) + ".json")
            reference = json.load(f)
            f.close()

            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["headers"], parsed_table.headings)

    def test_data(self):
        for table_index in range(1, 10):
            te = TableExtractor(DIR+"/tables/table_" + str(table_index) + ".tex")
            tp = TableParser()

            tables = te.extract_tables()
            if not tables:
                continue
            #self.assertTrue(len(tables) > 0)
            parsed_table = tp.parse(tables[0])

            f = open(DIR+"/references/cleaned_tables/table_" + str(table_index) + ".json")
            reference = json.load(f)
            f.close()

            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["rows"], parsed_table.data)

    def test_raw_data(self):
        for table_index in range(1, 11):
            if table_index == 5: continue
            te = TableExtractor(DIR+"/tables/table_" + str(table_index) + ".tex")
            tp = TableParser()

            tables = te.extract_tables()
            if not tables:
                continue
            #self.assertTrue(len(tables) > 0)
            parsed_table = tp.parse(tables[0], True)

            f = open(DIR+"/references/raw_tables/table_" + str(table_index) + ".json")
            reference = json.load(f)
            f.close()

            self.assertEqual(reference["<documentId>"]["<tableId>"]["table"]["rows"], parsed_table.data)


class TestTableExtraction(unittest.TestCase):
    def test_table_extraction(self):
        tables = sorted([DIR+'/tables/' + filename for filename in os.listdir(DIR+'/tables/') if os.path.isfile(os.path.join(DIR+'/tables/', filename))])
        outputDIR = DIR+'/output/'
        output = sorted([outputDIR + filename for filename in os.listdir(outputDIR) if os.path.isfile(os.path.join(outputDIR, filename))])
        extractor = TableExtractor(tables[0])
        with open(output[0]) as output:
            outputText = output.read()
        inputText = extractor.extract_tables()[0]
        self.assertEqual(inputText, outputText)


if __name__ == '__main__':
    unittest.main()
