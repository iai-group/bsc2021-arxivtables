__author__ = "Rebeca Pop"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser

if __name__ == "__main__":

    te = TableExtractor()
    tp = TableParser()

    f = open("../../tests/tables/multiple_tables.tex")
    latex_code = "".join(f.readlines())
    f.close()

    latex_tables = te.extract_tables(latex_code)

    for table in latex_tables:
        print(tp.parse(table).toJSON())   #.caption or .data or.headings


        #pt=tp.parse(table)
        #pt.(and you choose caption,data etc)
        #pt.caption="hvhdg" gives you error

