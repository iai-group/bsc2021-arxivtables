__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'

import os
import shutil
import requests

class ArxivGetter:
    """Module that contains classes to handle arXiv paper download and extract

    Args: paper_id: str

    Usage example:
    ag = ArxivGetter('2103.10359')\n
    paper = ag.get_paper()\n
    """

    def __init__(self, paper_id: str):
        self.paper_id = paper_id
        self.split_paper_id = self.paper_id.split('.')
        self.immutable = (self.split_paper_id[0][0:2],
                          self.split_paper_id[0][2:], self.split_paper_id[1])
        self.year, self.month, self.id = self.immutable

    def get_paper(self):
        """Retrieve .tar.gz source from arXiv given a specific paper ID,
        place to downloads directory.

        Args: None

        Returns:
            String of where extracted file is on the disk.

        Raises:
            None
        """
        if not os.path.exists('downloads/{}/{}/{}/{}.tar.gz'.format(
                self.year, self.month, self.id, self.paper_id)):
            result = requests.get(
                'https://arxiv.org/e-print/' + self.paper_id, stream='true')
            if result.status_code == 200:
                if not os.path.exists('downloads/{}/{}/{}'.format(
                        self.year, self.month, self.id)):
                    os.makedirs('downloads/{}/{}/{}'.format(
                        self.year, self.month, self.id), exist_ok=True)
                with open('downloads/{}/{}/{}/{}.tar.gz'.format(
                        self.year, self.month, self.id, self.paper_id),
                          'wb') as f:
                    f.write(result.raw.read())
                print('Downloaded and saved {}.tar.gz'.format(self.paper_id))
        if '{}.tar.gz'.format(self.paper_id) in os.listdir(
                'downloads/{}/{}/{}'.format(self.year, self.month, self.id)):
            return 'downloads/{}/{}/{}/{}.tar.gz'.format(
                self.year, self.month, self.id, self.paper_id)
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
            shutil.rmtree('downloads/{}/{}/{}/{}'.format(
                self.year, self.month, self.id, self.paper_id),
                ignore_errors=True)
            return True
        except Exception as e:
            print(e)
            return False

    def add_to_database(self):
        return 0
