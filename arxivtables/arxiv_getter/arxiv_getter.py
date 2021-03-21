__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'
__version__ = '0.1.0'

import time

import requests
import xmltodict
import json
import os
import tarfile


class ArxivGetter:
    def __init__(self):
        self.name = 'ArxivGetter'

    def get_latest_papers(self):
        result = requests.get(
            'http://export.arxiv.org/api/query?search_query=computer')
        as_json = xmltodict.parse(result.text)

        with open('results.json', 'w') as f:
            json.dump(as_json['feed']['entry'], f, indent=2)

    def get_paper_by_id(self, paper_id):
        """Retrieve .tar.gz source from arXiv given a specific paper ID, extract to downloads directory.

        :param paper_id:
        :return: Location on disk
        """
        result = requests.get(
            'https://arxiv.org/e-print/' + paper_id, stream='true')
        if result.status_code == 200:
            os.mkdir('downloads') if 'downloads' not in os.listdir('.') else True
            os.mkdir('downloads/' + paper_id) if paper_id not in os.listdir('downloads/') else True
            with open('downloads/' + paper_id + '/' + paper_id + '.tar.gz', 'wb') as f:
                f.write(result.raw.read())
            tar = tarfile.open('downloads/' + paper_id + '/' + paper_id + '.tar.gz', 'r:gz')
            tar.extractall('downloads/' + paper_id + '/')
            tar.extractall('downloads/' + paper_id + '/')
            tar.close()

        print('extracted')
        # SPLIT TO NEW FUNCTION
        time.sleep(5)
        for (dirpath, dirnames, filenames) in os.walk('downloads/' + paper_id):
            print(dirpath, dirnames, filenames)
            for filename in filenames:
                os.remove(dirpath+'/'+filename)
            try:
                os.rmdir(dirpath)
            except Exception as e:
                print(e)
        try:
            os.rmdir('downloads/' + paper_id) if paper_id in os.listdir('downloads/') else True
        except Exception as e:
            print(e)

    def add_to_database(self):
        return 0
