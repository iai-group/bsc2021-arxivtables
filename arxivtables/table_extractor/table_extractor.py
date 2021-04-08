__author__ = "David Ramsay"
__maintainer__ = "Rebeca Pop, David Ramsay"

import os
import tarfile
from TexSoup import TexSoup

class TableExtractor:
    def __init__(self, paper_id):
        self.name = 'Table Extractor for {}'.format(paper_id.split('/')[-1])
        self.paper_id = paper_id
        self.split_paper_id = self.paper_id.split('.')
        self.immutable = (self.split_paper_id[0][0:2], self.split_paper_id[0][2:], self.split_paper_id[1])
        self.year, self.month, self.id = self.immutable

    def extract_files(self):
        try:
            tar = tarfile.open('downloads/{}/{}/{}/{}.tar.gz'.format(self.year, self.month, self.id, self.paper_id),
                               'r:gz')
            tar.extractall('downloads/{}/{}/{}/{}'.format(self.year, self.month, self.id, self.paper_id))
            tar.close()
            print('extracted')
        except Exception as e:
            print(e)

    def extract_tables(self):
        tex_files = []
        for root, dirs, files in os.walk('downloads/{}/{}/{}/{}'.format(self.year, self.month, self.id, self.paper_id)):
            for file in files:
                if file.endswith('.tex'):
                    tex_files.append(root + '/' + file)
        all_tables = []
        for file_file in tex_files:
            with open(file_file) as file:
                soup = TexSoup(file)
            tables = list(soup.find_all('table'))
            tables_multi = list(soup.find_all('table*'))
            str_tables = tables + tables_multi
            all_tables += str_tables
        for index, table in enumerate(all_tables):
            all_tables[index] = str(table)
        return all_tables
