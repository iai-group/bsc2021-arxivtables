from arxivtables.arxiv_getter.arxiv_getter import ArxivGetter

print('Hello, World')

aGetter = ArxivGetter()

print(aGetter.name)

aGetter.getLatestPapers()
