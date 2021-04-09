import json
import os
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['db']
collection_arxiv_papers = db['arxiv_papers']

for (root, dir, files) in os.walk('db/arxiv_papers/'):
    for file in files:
        with open(root+file, 'r') as f:
            file_data = json.load(f)
        collection_arxiv_papers.insert_one(file_data)
        print(file + " inserted")

client.close()