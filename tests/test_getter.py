import unittest
from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter


class TestGetter(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGetter, self).__init__(*args, **kwargs)
        self.ag = ArxivGetter('2103.10359')

    def test_get(self):
        path = self.ag.get_paper()
        self.assertEqual(path, 'downloads/2103.10359')

    def test_delete_file_exist(self):
        deleted = self.ag.delete()
        self.assertEqual(deleted, True)

    def test_delete_file_not_exist(self):
        deleted = self.ag.delete()
        self.assertEqual(deleted, False)

    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
