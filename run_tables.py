__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'
__version__ = '0.1.0'
import os
#from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter
from arxivtables.arxiv_watcher.arxiv_watcher import ArxivWatcher

aw = ArxivWatcher()

paper_ids = aw.get_latest_paper_ids()

for id in paper_ids:
    ag = ArxivGetter(id)
    print(ag.paper_id)
    ag.get_paper()
