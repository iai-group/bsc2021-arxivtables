from pylatexenc.latex2text import LatexNodes2Text



class TableExtractor:
    def __init__(self):
        self.name = 'TableExtractor'

    def extractTables(self):
        return 0

    def table_to_text(self, latex_code):
        return LatexNodes2Text().latex_to_text(latex_code)

    def get_table_caption(self, latex_code):
        return 0
