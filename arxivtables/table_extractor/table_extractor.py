__author__ = "David Ramsay"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

from TexSoup import TexSoup
import tarfile
import os

class TableExtractor:
    def __init__(self, paper_id):
        self.name = 'Table Extractor for {}'.format(paper_id.split('/')[-1])
        self.paper_id = paper_id
        self.split_paper_id = self.paper_id.split('.')
        self.immutable = (self.split_paper_id[0][0:2], self.split_paper_id[0][2:], self.split_paper_id[1])
        self.year, self.month, self.id = self.immutable

    def extract_files(self):
        try:
            tar = tarfile.open('downloads/{}/{}/{}/{}.tar.gz'.format(self.year, self.month, self.id, self.paper_id), 'r:gz')
            tar.extractall('downloads/{}/{}/{}/{}'.format(self.year, self.month, self.id, self.paper_id))
            tar.close()
            print('extracted')
        except Exception as e:
            print(e)

    def extract_tables(self):
        texFiles = []
        for root, dirs, files in os.walk('downloads/{}/{}/{}/{}'.format(self.year, self.month, self.id, self.paper_id)):
            for file in files:
                if file.endswith('.tex'):
                    texFiles.append(root + '/' +file)
        allTables = []
        for fileFile in texFiles:
            #with open(self.paper_id) as file:
            with open(fileFile) as file:
                soup = TexSoup(file)
            tables = list(soup.find_all('table'))
            tablesMulti = list(soup.find_all('table*'))
            strTables = tables + tablesMulti
            allTables += strTables
        for index, table in enumerate(allTables):
            allTables[index] = str(table)
        return allTables
