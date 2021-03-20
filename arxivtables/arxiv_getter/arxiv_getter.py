__author__ = "David Ramsay"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"

import requests
import xmltodict
import json
import os
import tarfile


class ArxivGetter:
    def __init__(self):
        self.name = 'ArxivGetter'

    def getLatestPapers(self):
        result = requests.get(
            "http://export.arxiv.org/api/query?search_query=computer")
        asJson = xmltodict.parse(result.text)

        with open('results.json', 'w') as f:
            json.dump(asJson["feed"]["entry"], f, indent=2)

    def getPaperById(self, id):
        result = requests.get(
            "https://arxiv.org/e-print/"+id, stream="true")
        if result.status_code == 200:
            os.mkdir("downloads") if "downloads" not in os.listdir(".") else True
            os.mkdir("downloads/"+id) if id not in os.listdir("downloads/") else True
            with open("downloads/"+id+"/"+id+".tar.gz", "wb") as f:
                f.write(result.raw.read())
        tar = tarfile.open("downloads/"+id+"/"+id+".tar.gz", "r:gz")
        tar.extractall("downloads/"+id+"/")
        tar.close()
        return 0

    def addToDatabase(self):
        return 0
