__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'

import unittest
from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter


class TestGetter(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGetter, self).__init__(*args, **kwargs)
        self.ag = ArxivGetter('2103.10359')

    def test_get(self):
        path = self.ag.get_paper()
        self.assertEqual(path, 'downloads/21/03/10359/2103.10359.tar.gz')

    def test_delete_file_exist(self):
        deleted = self.ag.delete()
        self.assertTrue(deleted)

    def test_delete_file_not_exist(self):
        deleted = self.ag.delete()
        self.assertFalse(deleted)


if __name__ == '__main__':
    unittest.main()
