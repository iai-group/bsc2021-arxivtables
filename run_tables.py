__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'

import os
import json
import argh
import yaml
from datetime import datetime
from pymongo import MongoClient
from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter
from arxivtables.arxiv_watcher.arxiv_watcher import ArxivWatcher
from arxivtables.table_extractor.table_extractor import TableExtractor
from arxivtables.table_extractor.table_parser import TableParser

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

if cfg["other"]["date"]["use_date"]:
    date = cfg["other"]["date"]["date"]
else:
    date = str(datetime.date(datetime.now())).replace('-', '')


def set_up_mongo(url):
    """Simple MongoDB client setup

    Args:
        url:
            String of MongoDB url.
    Returns:
        client: MongoDB client
        db: MongoDB client db
        collection: MongoDB client db collection
    Raises:
        None
    """
    client = MongoClient(url, 27017)
    db = client['db']
    collection = db['arxiv_papers']
    return client, db, collection


def run_tables(
        downloader_date=date, mongo=cfg["mongodb"]["use_mongo"],
        url=cfg["mongodb"]["url"]
        ):
    """
    Main method that handles fetching, downloading, extracting, and saving
    arXiv data.

    Args:
        downloader_date:
            (optional) Date of log file to run table extraction, YYYMMDD format.
            Defaults to current date.
        mongo:
            (optional) Boolean flag to signal use of MongoDB.
            Defaults to False.
        url:
            If using MongoDB, supply url.
            Likely 'database' or 'localhost'.
            Defaults to 'localhost'.
    Returns:
        No return
    Raises:
        Exception
    """
    if mongo:
        client, db, collection_arxiv_papers = set_up_mongo(url)

    aw = ArxivWatcher()

    if downloader_date == str(datetime.date(datetime.now()))\
            .replace('-', ''):
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
            with open(
                    'db/arxiv_papers/{}/{}/{}.json'.format(
                            p_id[0:2], p_id[2:4], p_id
                    )
            ) as j:
                paper_dict = json.load(j)
            for table in tables:
                try:
                    parsed = tp.parse(table)
                    paper_dict["tables"].append(parsed.toJSON())
                except Exception as e:
                    print(e)
            print(paper_dict)
            with open(
                    'db/arxiv_papers/{}/{}/{}.json'.format(
                            p_id[0:2], p_id[2:4], p_id
                    ), 'w'
            ) as j:
                j.write(json.dumps(paper_dict, indent=2))
            if mongo:
                collection_arxiv_papers.replace_one(
                    {'p_id': p_id}, paper_dict, upsert=True
                )
                print(p_id + " inserted")
            paper_dict = None
        except Exception as e:
            print(e)
        ag.delete()
    if mongo:
        client.close()


if __name__ == '__main__':
    argh.dispatch_command(run_tables)
