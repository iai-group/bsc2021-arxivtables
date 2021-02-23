__author__ = "David Ramsay"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

#from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter
from arxivtables.table_extractor.table_extractor import TableExtractor
import os


DIR = os.path.dirname(os.path.realpath(__file__))+'/tests/tables/'

if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/output/'):
    os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '/output/')

tables = sorted([DIR + filename for filename in os.listdir(
    DIR) if os.path.isfile(os.path.join(DIR, filename))])

for table in tables:
    extractor = TableExtractor(table)
    extractor.extractTables(
        os.path.dirname(os.path.realpath(__file__)) + '/output/')
