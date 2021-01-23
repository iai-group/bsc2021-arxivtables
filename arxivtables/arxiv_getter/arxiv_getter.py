import requests
import xmltodict
import json


class ArxivGetter:
    def __init__(self):
        self.name = 'Gimme tables'

    def getLatestPapers(self):
        result = requests.get(
            "http://export.arxiv.org/api/query?search_query=computer")
        asJson = xmltodict.parse(result.text)

        with open('results.json', 'w') as f:
            json.dump(asJson, f, indent=2)
