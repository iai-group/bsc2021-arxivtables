__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'

import os
import json
import requests
from datetime import datetime
from xml.etree.ElementTree import fromstring
import proto.proto.tables_pb2 as table_proto


class ArxivWatcher:
    def __init__(self):
        self.previously_loaded_ids = self.read_previously_loaded_ids()
        self.current_date = str(datetime.date(datetime.now())).replace('-', '')

    def read_previously_loaded_ids(self):
        """Read previously loaded IDs from the log file

            Args: None

            Returns:
                IDs of papers previously loaded as list of strings

            Raises: Nothing
        """
        if not os.path.exists('logs/downloader'):
            os.mkdir('logs/downloader')
        try:
            with open('logs/downloader/previously_loaded_ids.log', 'r') as f:
                ids = f.readlines()
        except:
            ids = []
        return [p_id[:-1] for p_id in ids]

    def get_latest_papers(self):
        """Retrieve list of latest submissions on arXiv.org, return in

                Args: None

                Returns:
                    String of where extracted files are on the disk.

                Raises:

        """
        base_url = 'http://export.arxiv.org/api/query?'
        query = \
            'search_query=all:all&' \
            'sortBy=submittedDate&' \
            'sortOrder=descending&' \
            'max_results=500'
        result = requests.get(base_url + query)
        with open('logs/downloader/{}.log'.format(
                self.current_date), 'a') as f:
            f.write('')
        if result.status_code == 200:
            paper = table_proto.Paper()
            string_xml = result.content
            tree = fromstring(string_xml)
            for child in tree[len(tree):0:-1]:
                if child.tag == "{http://www.w3.org/2005/Atom}entry":
                    entry_authors = []
                    for c in child:
                        if c.tag == "{http://www.w3.org/2005/Atom}id":
                            entry_id, entry_url = c.text, c.text
                        entry_id = entry_id.split('/')[-1].split('v')[0]
                        if c.tag == "{http://www.w3.org/2005/Atom}title":
                            entry_title = c.text
                        if c.tag == "{http://www.w3.org/2005/Atom}published":
                            entry_published = c.text
                        if c.tag == "{http://www.w3.org/2005/Atom}author":
                            entry_authors.append(c[0].text)
                    entry = {
                        "p_id": entry_id,
                        "title": entry_title,
                        "dateFetched": str(datetime.date(datetime.now())),
                        "authors": entry_authors,
                        "href": entry_url,
                        "publicationDate": entry_published,
                        "tables": []
                    }

                    if entry_id not in self.previously_loaded_ids:
                        with open(
                                'logs/downloader/previously_loaded_ids.log',
                                'a'
                        ) as f:
                            f.write(entry_id)
                            f.write('\n')
                        with open('logs/downloader/{}.log'.format(
                                self.current_date), 'a') as f:
                            f.write(entry_id)
                            f.write('\n')
                        if not os.path.exists('db/arxiv_papers/{}/{}'.format(
                                entry_id[0:2], entry_id[2:4])):
                            os.makedirs('db/arxiv_papers/{}/{}'.format(
                                entry_id[0:2], entry_id[2:4]), exist_ok=True)
                    paper.p_id = entry_id
                    paper.title = entry_title
                    paper.dateFetched = str(datetime.date(datetime.now()))
                    for author in entry_authors:
                        paper.authors.append(author)
                    paper.href = entry_url
                    paper.publicationDate = entry_published
                    with open('db/arxiv_papers/{}/{}/{}'.format(
                            entry_id[0:2], entry_id[2:4], entry_id), 'wb') as f:
                        f.write(paper.SerializeToString())
        else:
            print("Status code: " + result.status_code)

    def get_ids_from_log(self, date=None):
        """
            Args:
                date - Date string in YYYMMDD format

            Returns:
                Array of stings representing ID

            Raises:
                FileNotFoundError
        """
        if date is None:
            date = self.current_date
        try:
            with open('logs/downloader/{}.log'.format(date), 'r') as f:
                ids = f.readlines()
            return [pid[:-1] for pid in ids]
        except FileNotFoundError:
            raise FileNotFoundError
