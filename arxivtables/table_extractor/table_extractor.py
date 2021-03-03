__author__ = "David Ramsay"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

from TexSoup import TexSoup

class TableExtractor:
    def __init__(self, input_file):
        self.name = 'Table Extractor for {}'.format(input_file.split('/')[-1])
        self.input_file = input_file

    def extract_tables(self):
        with open(self.input_file) as file:
            soup = TexSoup(file)
        tables = list(soup.find_all('table'))
        tablesMulti = list(soup.find_all('table*'))
        strTables = [*[str(table) for table in tables], *[str(table) for table in tablesMulti]]
        return strTables

