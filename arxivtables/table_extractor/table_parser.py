__author__ = "Rebeca Pop"
__maintainer__ = "Rebeca Pop, David Ramsay"
__version__ = "0.1.0"


from arxivtables.table_extractor.parsed_table import ParsedTable
from astropy.io import ascii
from tex2py import tex2py
from pylatexenc.latex2text import LatexNodes2Text


class TableParser:
    def __init__(self):
        self.name = 'TableParser'

    def parse(self, latex_source : str) -> ParsedTable:
        latex_source = self.sanitize_table_lines(latex_source)

        content = tex2py(latex_source)
        caption_str = str(content.source.find("caption"))

        table_dict = dict()
        table_dict["caption"] = caption_str[caption_str.find("{") + 1: len(caption_str) - 1]

        astro_table = ascii.read(latex_source, format="latex")

        table_dict["headings"] = self.sanitize_latex_text_list(list(astro_table.columns))
        table_dict["data"] = []

        for row in astro_table:
            table_dict["data"].append(self.sanitize_latex_text_list(list(row)))

        return ParsedTable(table_dict)



    def sanitize_table_lines(self, latex_source : str) -> str:
        toprule_pos = latex_source.find("\\toprule")
        midrule_pos = latex_source.find("\\midrule")
        botrule_pos = latex_source.find("\\bottomrule")

        if toprule_pos == -1 or midrule_pos == -1 or botrule_pos == -1:
            return latex_source

        old_heading = latex_source[toprule_pos + len("\\toprule") + 1:midrule_pos - 2]
        heading = old_heading.replace("&\n", "&")

        old_rows = latex_source[midrule_pos + len("\\midrule") + 1:botrule_pos - 2]
        rows = old_rows.replace("&\n", "&")

        return latex_source.replace(old_heading, heading).replace(old_rows, rows)



    def sanitize_latex_text_list(self, strlist : list):
        result_list = []
        for x in strlist:
            result_list.append(self.sanitize_latex_text(str(x)))
        return result_list

    def sanitize_latex_text(self, latex_source : str) -> str:
        return LatexNodes2Text().latex_to_text(latex_source)
