import json
from pathlib import Path
from xml.etree.ElementTree import fromstring
import requests
from datetime import datetime
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class ArxivWatcher:
    def __init__(self):
        self.previosuly_loaded_ids = self.read_previously_loaded_ids()

    def read_previously_loaded_ids(self):
        Path('logs/downloader').mkdir(parents=True, exist_ok=True)
        try:
            with open(os.path.join(base_dir, 'logs/downloader/') + 'previously_loaded_ids.txt', 'r') as f:
                ids = f.readlines()
        except:
            ids = []
        return [id[:-1] for id in ids]

    def initialize_json_file(self, id, authors):
        return 0

    def get_latest_papers(self):
        """Retrieve list of latest submissions on arXiv.org, return in

                Args: None

                Returns:
                    String of where extracted files are on the disk.

                Raises:

                """
        base_url = 'http://export.arxiv.org/api/query?'
        query = 'search_query=all:all&sortBy=submittedDate&sortOrder=descending&max_results=50'
        result = requests.get(base_url + query)
        if result.status_code == 200:
            string_xml = result.content
            tree = fromstring(string_xml)
            for child in tree[len(tree):0:-1]:
                if child.tag == "{http://www.w3.org/2005/Atom}entry":
                    entry_authors = []
                    for c in child:
                        if c.tag == "{http://www.w3.org/2005/Atom}id": entry_id, entry_url = c.text, c.text
                        entry_url = entry_id
                        entry_id = entry_id.split('/')[-1].split('v')[0]
                        if c.tag == "{http://www.w3.org/2005/Atom}title": entry_title = c.text
                        if c.tag == "{http://www.w3.org/2005/Atom}published": entry_published = c.text
                        if c.tag == "{http://www.w3.org/2005/Atom}author": entry_authors.append(c[0].text)
                    entry = {
                        "id": entry_id,
                        "title": entry_title,
                        "dateFetched": str(datetime.date(datetime.now())),
                        "authors": entry_authors,
                        "href": entry_url,
                        "publicationDate": entry_published,
                        "tables": []
                    }

                    if (entry_id) not in self.previosuly_loaded_ids:
                        with open(os.path.join(base_dir, 'logs/downloader/') + 'previously_loaded_ids.txt', 'a') as f:
                            f.write(entry_id)
                            f.write('\n')
                        with open(os.path.join(base_dir, 'logs/downloader/') + str(datetime.date(datetime.now())).replace('-', '') + '.txt', 'a') as f:
                            f.write(entry_id)
                            f.write('\n')
                    Path('db/arxiv_papers').mkdir(parents=True, exist_ok=True)
                    with open(os.path.join(base_dir, 'db/arxiv_papers/') + entry_id + '.json', 'w') as f:
                        json.dump(entry, f, indent=2)

                print(entry_authors)
        else:
            print("Status code: " + result.status_code)

        with open(os.path.join(base_dir, 'logs/downloader/') + str(datetime.date(datetime.now())).replace('-', '') + '.txt', 'r') as f:
            ids = f.readlines()
        return [pid[:-1] for pid in ids]
