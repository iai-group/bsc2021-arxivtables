import xml.etree.ElementTree as ET
import requests


class ArxivWatcher:
    def __init__(self):
        self.previosuly_loaded_ids = self.read_previously_loaded_ids()

    def read_previously_loaded_ids(self):
        with open('previously_loaded_ids.txt', 'r') as f:
            ids = f.readlines()
        return ids

    def get_latest_papers(self):
        result = requests.get(
            'http://export.arxiv.org/api/query?search_query=all:all&sortBy=submittedDate&sortOrder=descending&max_results=100')
        if result.status_code == 200:
            string_xml = result.content
            tree = ET.fromstring(string_xml)
            for child in tree[len(tree):0:-1]:
                if child.tag == "{http://www.w3.org/2005/Atom}entry":
                    for c in child:
                        if c.tag == "{http://www.w3.org/2005/Atom}id": entryId = c.text
                        if c.tag == "{http://www.w3.org/2005/Atom}title": entryTitle = c.text
                        if c.tag == "{http://www.w3.org/2005/Atom}published": entryPublished = c.text
                    if entryId not in self.previosuly_loaded_ids:
                        with open('previously_loaded_ids.txt', 'a') as f:
                            f.write(entryId + '\n')
                    print("{}: {} published on {}".format(entryId, entryTitle, entryPublished))
                    print()

            with open('response.xml', 'wb') as f:
                f.write(result.content)
        else:
            print("Status code: " + result.status_code)


a = ArxivWatcher()

print(a.previosuly_loaded_ids)

a.get_latest_papers()
