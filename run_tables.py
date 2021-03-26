__author__ = "David Ramsay"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

#from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter
from arxivtables.table_extractor.table_extractor import TableExtractor
import os


DIR = os.path.dirname(os.path.realpath(__file__))+'/tests/tables/'

if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/tests/references/output/'):
    os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '/tests/references/output/')

tables = sorted([filename for filename in os.listdir(
    DIR) if os.path.isfile(os.path.join(DIR, filename))])

print(tables)

for table in tables:
    with open('tests/references/output/' + table.split('.')[0] + '.txt', 'w') as f:
        extractor = TableExtractor('tests/tables/' + table)
        extracted = extractor.extract_tables()
        for item in extracted:
            f.write(item)
