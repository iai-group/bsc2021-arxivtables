__author__ = "Rebeca Pop"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

import json
import unittest
import os
import os.path
from astropy.table import Table
from arxivtables.table_extractor.table_extractor import TableExtractor
from tex2py import tex2py

from arxivtables.table_extractor.table_parser import TableParser



class TestStringMethods(unittest.TestCase):
    DIR = os.path.dirname(os.path.realpath(__file__))+'/tables/'

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

    def test_if_there_is_an_input_and_an_output_directory(self):
        files = os.listdir()
        self.assertEqual("tables" in files and "references" in files, True)

    def test_extracted_tables_against_JSON_reference(self):
        extractor = TableExtractor()
        files = os.listdir(self.DIR)

        with open(self.DIR + "table_6.tex") as f:
            # content = f.read()
            # text=extractor.table_to_text(content.decode("utf-8"))
            # print(text)
            json = dict()
            content = tex2py(f)
            caption_str = str(content.source.find("caption"))  #.find("caption")
            json["caption"] = caption_str[caption_str.find("{") + 1: len(caption_str) - 2]

            #for line in f.readlines():
            #
            #    line_str = line.decode("utf-8")
            #
            #    if "caption{" in line_str :
            #        json["caption"] = line_str[line_str.find("{") + 1: len(line_str) - 2]

        print(json)
        self.assertEqual(True, True)

    def test_caption(self):
        for table_index in range(6, 11):
            f = open("tables/table_" + str(table_index) + ".tex")
            latex_code = "".join(f.readlines())
            f.close()

            te = TableExtractor()
            tp = TableParser()

            tables = te.extract_tables(latex_code)
            parsed_table = tp.parse(tables[0])

            f = open("references/JSON_representation_" + str(table_index) + ".json")
            reference = json.load(f)
            f.close()

            self.assertEqual(reference["metadata"]["caption"], parsed_table.caption)


    def test_headings(self):
        for table_index in range(6, 11):
            f = open("tables/table_" + str(table_index) + ".tex")
            latex_code = "".join(f.readlines())
            f.close()

            te = TableExtractor()
            tp = TableParser()

            tables = te.extract_tables(latex_code)
            parsed_table = tp.parse(tables[0])

            f = open("references/JSON_representation_" + str(table_index) + ".json")
            reference = json.load(f)
            f.close()

            self.assertEqual(reference["headings"], parsed_table.headings)


    def test_data(self):
        for table_index in range(6, 11):
            f = open("tables/table_" + str(table_index) + ".tex")
            latex_code = "".join(f.readlines())
            f.close()

            te = TableExtractor()
            tp = TableParser()

            tables = te.extract_tables(latex_code)
            parsed_table = tp.parse(tables[0])

            f = open("references/JSON_representation_" + str(table_index) + ".json")
            reference = json.load(f)
            f.close()

            self.assertEqual(reference["data"], parsed_table.data)

if __name__ == '__main__':
    unittest.main()
