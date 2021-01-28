import requests
import xmltodict
import json


class ArxivGetter:
    def __init__(self):
        self.name = 'ArxivGetter'

    def getLatestPapers(self):
        result = requests.get(
            "http://export.arxiv.org/api/query?search_query=computer")
        asJson = xmltodict.parse(result.text)

        with open('results.json', 'w') as f:
            json.dump(asJson["feed"]["entry"], f, indent=2)

    def download(self):
        return 0

    def addToDatabase(self):
        return 0
