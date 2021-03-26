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
    """Module that contains classes to handle arXiv paper download and extract

    Usage example:
    ag = ArxivGetter('2103.10359')\n
    paper = ag.get_paper()\n
    """
    def __init__(self, paper_id: str):
        self.paper_id = paper_id

    def get_paper(self):
        """Retrieve .tar.gz source from arXiv given a specific paper ID, extract to downloads directory.

        Args: None

        Returns:
            String of where extracted files are on the disk.

        Raises:

        """
        result = requests.get(
            'https://arxiv.org/e-print/' + self.paper_id, stream='true')
        if result.status_code == 200:
            os.mkdir('downloads') if 'downloads' not in os.listdir('.') else True
            os.mkdir('downloads/' + self.paper_id) if self.paper_id not in os.listdir('downloads/') else True
            with open('downloads/' + self.paper_id + '/' + self.paper_id + '.tar.gz', 'wb') as f:
                f.write(result.raw.read())
            tar = tarfile.open('downloads/' + self.paper_id + '/' + self.paper_id + '.tar.gz', 'r:gz')
            tar.extractall('downloads/' + self.paper_id + '/')
            tar.close()
        print('extracted')
        if self.paper_id in os.listdir('downloads'):
            return 'downloads/' + self.paper_id
        else:
            return False

    def delete(self):
        """Delete all files related to  paper of 'paper_id'.

        Args: None

        Returns:
            Boolean.  True if all files delete, false if not.

        Raises:
            FileNotFoundError
        """
        try:
            if self.paper_id not in os.listdir('downloads'):
                return False
            for (dirpath, dirnames, filenames) in os.walk('downloads/' +  self.paper_id):
                for filename in filenames:
                    os.remove(dirpath+'/'+filename)
                try:
                    os.rmdir(dirpath)
                except FileNotFoundError:
                    print("File not found")
                    return False
                except Exception as e:
                    print(e)
                os.rmdir('downloads/' + self.paper_id) if self.paper_id in os.listdir('downloads/') else True
            return True
        except FileNotFoundError:
            print("File not found")
            return False
        except Exception as e:
            print(e)


    def add_to_database(self):
        return 0
