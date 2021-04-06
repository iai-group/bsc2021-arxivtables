__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'
__version__ = '0.1.0'

import json
import os
from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter
from arxivtables.arxiv_watcher.arxiv_watcher import ArxivWatcher
from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser

aw = ArxivWatcher()

paper_ids = aw.get_latest_papers()

for index, id in enumerate(paper_ids):
    print('[Item {} of {}]'.format(index+1, len(paper_ids)))
    ag = ArxivGetter(id)
    print(ag.paper_id)
    ag.get_paper()
    te = TableExtractor(id)
    try:
        te.extract_files()
        tables = te.extract_tables()
        if tables is None:
            continue
        tp = TableParser()
        parsed = None
        paperDict = None
        with open('db/arxiv_papers/' +  id +'.json') as j:
            paperDict = json.load(j)
        for table in tables:
            parsed = tp.parse(table)
            paperDict["tables"].append(parsed.toJSON())
        with open('db/arxiv_papers/' + id + '.json', 'w') as j:
            json.dump(paperDict, j, indent=2)
            paperDict = None

    except Exception as e:
        print(e)
        continue

for jsonFile in os.listdir('db/arxiv_papers/'):
    with open('db/arxiv_papers/'+jsonFile) as jf:
        jf = json.load(jf)
        if len(jf["tables"]) > 0:
            print(jsonFile)
