__author__ = 'David Ramsay'

from pymongo import MongoClient
import argh


def find_results_with_tables(url='localhost', date='YYYY-MM-DD'):
    try:
        client = MongoClient(url, 27017)
        db = client['db']
        collection = db['arxiv_papers']
        for x in collection.find({
                                    'dateFetched': date, "$where":
                """this.tables.length > 1"""
                                },{"p_id"}):
            print(x["p_id"])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    argh.dispatch_command(find_results_with_tables)
