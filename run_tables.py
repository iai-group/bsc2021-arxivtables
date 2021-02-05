#from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter
from arxivtables.table_extractor.table_extractor import TableExtractor
import os


DIR = os.getcwd()+'/tests/tables/'

tables = sorted([DIR + filename for filename in os.listdir(
    DIR) if os.path.isfile(os.path.join(DIR, filename))])

for table in tables:
    extractor = TableExtractor(table)
    print(extractor.find_all_table_indices())
