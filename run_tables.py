__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'

import os
import json
import argh
from datetime import datetime
from pymongo import MongoClient
from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter
from arxivtables.arxiv_watcher.arxiv_watcher import ArxivWatcher
from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser


def set_up_mongo(url='localhost'):
    """"Simple
    """
    client = MongoClient(url, 27017)
    db = client['db']
    collection = db['arxiv_papers']
    return client, db, collection


def run_tables(downloader_date=str(datetime.date(datetime.now())).replace('-', ''), mongo=False, url='localhost'):
    """"Main method that handles fetching, downloading, extracting, and saving arXiv data.

    Args:
        downloader_date:
            (optional) Date of log file to run table extraction on, in YYYMMDD format.
            Defaults to current date.
        mongo:
            (optional) Boolean flag to signal use of MongoDB.
            Defaults to False.
        url:
            If using MongoDB, supply url.  Likely 'database' (if using Docker) or 'localhost' (if running local).
            Defaults to 'localhost'.
    Returns:
        No return
    Raises:
        Exception
    """
    if mongo:
        client, db, collection_arxiv_papers = set_up_mongo(url)

    aw = ArxivWatcher()

    if downloader_date == str(datetime.date(datetime.now())).replace('-', ''):
        aw.get_latest_papers()

    paper_ids = aw.get_ids_from_log(downloader_date)

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
                try:
                    parsed = tp.parse(table)
                    paper_dict["tables"].append(parsed.toJSON())
                except Exception as e:
                    print(e)
            with open('db/arxiv_papers/' + p_id + '.json', 'w') as j:
                json.dump(paper_dict, j, indent=2)
            if mongo:
                collection_arxiv_papers.replace_one({'p_id': p_id}, paper_dict, upsert=True)
                print(p_id + " inserted")
            paper_dict = None
        except Exception as e:
            print(e)
        ag.delete()
    if mongo:
        client.close()

    for jsonFile in os.listdir('db/arxiv_papers/'):
        with open('db/arxiv_papers/' + jsonFile) as jf:
            jf = json.load(jf)
            if len(jf["tables"]) > 0:
                print(jsonFile)


if __name__ == '__main__':
    argh.dispatch_command(run_tables)
