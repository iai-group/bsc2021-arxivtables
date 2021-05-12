import re

from TexSoup import TexSoup
from astropy.io.ascii import InconsistentTableError
from pylatexenc.latex2text import LatexNodes2Text
from tex2py import tex2py
from astropy.io import ascii
from arxivtables.table_extractor.table_parser import TableParser


def sanitize_table_lines(latex_source: str) -> str:
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

    old_heading = latex_source[
                  toprule_pos + len("\\toprule") + 1:midrule_pos - 2]
    heading = old_heading.replace("&\n", "&")

    old_rows = latex_source[
               midrule_pos + len("\\midrule") + 1:botrule_pos - 2]
    rows = old_rows.replace("&\n", "&")

    return latex_source.replace(
        old_heading, heading
    ).replace(old_rows, rows)


def sanitize_latex_text_list(strlist: list):
    result_list = []
    for x in strlist:
        result_list.append(sanitize_latex_text(str(x)))
    return result_list


def sanitize_latex_text(latex_source: str) -> str:
    return LatexNodes2Text().latex_to_text(latex_source)


tp = TableParser()
with open('multirow.tex') as file:
    source = TexSoup(file)

#print(source.multicolumn.args[0])
#print(list(source.find_all('table'))[0])

src = sanitize_table_lines(str(list(source.find_all('table'))[0]))
t2p = tex2py(src)

print(src)
print('---------------')

multirow_pattern = r'\\multirow{([0-9])}{(.*?)}{(.*?)}'
empty_segment = ' & '
split_src = src.splitlines()

try:
    astro_table = ascii.read(src, format="latex")
except InconsistentTableError:
    print("ITE")
    print('---------------')

for line in split_src:
    orig_line = line
    index = split_src.index(line)
    result = re.findall(multirow_pattern, line)
    if result:
        print(index)
        print(result)
        for r in result:
            (rows, alignment, text) = r
            #new_line = text + empty_segment * (int(rows) - 1)
            line = line.replace(
                '\\multirow{' + rows + '}{' + alignment + '}{'
                                                                '' + text + '}',
                text
                )

            #print(new_line)
            split_src[index] = line
            print(split_src[index])
print('---------------')
print(split_src)
src = "\n".join(split_src)
print(src)
print('---------------')

try:
    astro_table = ascii.read(src, format="latex")
except InconsistentTableError:
    print("ITE")
