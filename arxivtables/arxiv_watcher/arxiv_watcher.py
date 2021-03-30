from xml.etree.ElementTree import fromstring
import requests
from datetime import datetime
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class ArxivWatcher:
    def __init__(self):
        self.previosuly_loaded_ids = self.read_previously_loaded_ids()

    def read_previously_loaded_ids(self):
        with open(base_dir + '\\logs\\downloader\\previously_loaded_ids.txt', 'r') as f:
            ids = f.readlines()
        return [id[:-1] for id in ids]

    def get_latest_paper_ids(self):
        """Retrieve list of latest submissions on arXiv.org, return in

                Args: None

                Returns:
                    String of where extracted files are on the disk.

                Raises:

                """
        base_url = 'http://export.arxiv.org/api/query?'
        query = 'search_query=all:all&sortBy=submittedDate&sortOrder=descending&max_results=500'
        result = requests.get(base_url + query)
        if result.status_code == 200:
            string_xml = result.content
            tree = fromstring(string_xml)
            for child in tree[len(tree):0:-1]:
                if child.tag == "{http://www.w3.org/2005/Atom}entry":
                    for c in child:
                        if c.tag == "{http://www.w3.org/2005/Atom}id": entry_id = c.text
                        entry_url = entry_id
                        entry_id = entry_id.split('/')[-1].split('v')[0]
                        if c.tag == "{http://www.w3.org/2005/Atom}title": entry_title = c.text
                        if c.tag == "{http://www.w3.org/2005/Atom}published": entry_published = c.text
                    if (entry_id) not in self.previosuly_loaded_ids:
                        with open(base_dir + '\\logs\\downloader\\previously_loaded_ids.txt', 'a') as f:
                            f.write(entry_id)
                            f.write('\n')
                        with open(base_dir + '\\logs\\downloader\\' + str(datetime.date(datetime.now())).replace('-', '') + '.txt', 'a') as f:
                            f.write(entry_id)
                            f.write('\n')
        else:
            print("Status code: " + result.status_code)

        with open(base_dir + '\\logs\\downloader\\' + str(datetime.date(datetime.now())).replace('-', '') + '.txt', 'r') as f:
            ids = f.readlines()
        return [id[:-1] for id in ids]