__author__ = 'David Ramsay'
__maintainer__ = 'Rebeca Pop, David Ramsay'
__version__ = '0.1.0'

from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter

ag = ArxivGetter()

if __name__ == '__main__':
    ag.get_paper_by_id('2103.10359')
