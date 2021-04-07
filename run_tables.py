__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'
__version__ = '0.1.0'

import json
import os
from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter
from arxivtables.arxiv_watcher.arxiv_watcher import ArxivWatcher
from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['db']
collection_arxiv_papers = db['arxiv_papers']

aw = ArxivWatcher()

paper_ids = aw.get_latest_papers()

for index, p_id in enumerate(paper_ids):
    print('[Item {} of {}]'.format(index + 1, len(paper_ids)))
    ag = ArxivGetter(p_id)
    print(ag.paper_id)
    ag.get_paper()
    te = TableExtractor(p_id)
    try:
        te.extract_files()
        tables = te.extract_tables()
        if tables is None:
            continue
        tp = TableParser()
        parsed = None
        paper_dict = None
        with open('db/arxiv_papers/' + p_id + '.json') as j:
            paper_dict = json.load(j)
        for table in tables:
            parsed = tp.parse(table)
            paper_dict["tables"].append(parsed.toJSON())
        with open('db/arxiv_papers/' + p_id + '.json', 'w') as j:
            json.dump(paper_dict, j, indent=2)

        collection_arxiv_papers.insert_one(paper_dict)
        print(p_id + " inserted")
        paper_dict = None
    except Exception as e:
        print(e)
    ag.delete()
client.close()

for jsonFile in os.listdir('db/arxiv_papers/'):
    with open('db/arxiv_papers/' + jsonFile) as jf:
        jf = json.load(jf)
        if len(jf["tables"]) > 0:
            print(jsonFile)
