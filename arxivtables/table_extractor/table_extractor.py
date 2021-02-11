class TableExtractor:
    def __init__(self):
        self.name = 'TableExtractor'


    def extract_tables(self, latex_code : str):
        start_pos = 0

        tables = []
        while start_pos >= 0:
            start_pos = latex_code.find("\\begin{table", start_pos)
            if start_pos == -1:
                break

            end_pos = latex_code.find("\\end{table", start_pos)

            close_bracket_pos = latex_code.find("}", end_pos)

            tables.append(latex_code[start_pos:end_pos+(close_bracket_pos-end_pos+1)])
            start_pos = end_pos

        return tables
