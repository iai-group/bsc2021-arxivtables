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

    def parse(self, latex_source : str, is_raw : bool = False) -> ParsedTable:
        latex_source = self.__sanitize_table_lines(latex_source)
        content = tex2py(latex_source)

        caption_source = content.source.find("caption")
        if not caption_source:
            caption = ""
        else:
            caption_str = str(caption_source)
            caption = caption_str[caption_str.find("{") + 1: len(caption_str) - 1]

            if not is_raw:
                caption = self.__sanitize_latex_text(caption).strip()

        astro_table = ascii.read(latex_source, format="latex")

        headings = list(map(str, list(astro_table.columns)))
        if not is_raw:
            headings = self.__sanitize_latex_text_list(headings)

        data = []
        for row in astro_table:
            row_items = list(map(str, list(row)))
            if not is_raw:
                row_items = self.__sanitize_latex_text_list(row_items)
            data.append(row_items)

        return ParsedTable(caption, headings, data)

    def __sanitize_table_lines(self, latex_source : str) -> str:
        lines = latex_source.split("\n")
        new_source = ""
        for l in lines:
            if l.strip():
                new_source += l + "\n"
        latex_source = new_source

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

    def __sanitize_latex_text_list(self, strlist : list):
        result_list = []
        for x in strlist:
            result_list.append(self.__sanitize_latex_text(str(x)))
        return result_list


    def __sanitize_latex_text(self, latex_source : str) -> str:
        return LatexNodes2Text().latex_to_text(latex_source)
