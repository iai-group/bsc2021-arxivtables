class TableExtractor:
    def __init__(self, input_file):
        self.name = 'Table Extractor for {}'.format(input_file.split('/')[-1])
        self.input_file = input_file
        self.begin_table_indices = []
        self.end_table_indices = []

    def extract_tables(self, latex_code: str):
        start_pos = 0

        tables = []
        while start_pos >= 0:
            start_pos = latex_code.find("\\begin{table", start_pos)
            if start_pos == -1:
                break

            end_pos = latex_code.find("\\end{table", start_pos)
            close_bracket_pos = latex_code.find("}", end_pos)

            tables.append(
                latex_code[start_pos:end_pos+(close_bracket_pos-end_pos+1)])
            start_pos = end_pos

        return tables

    def find_all_table_indices(self):
        lines = []
        #if self.check_if_valid():
        with open(self.input_file) as f:
            lines = f.readlines()
        try:
            self.begin_table_indices = [lines.index(
                l) for l in lines if '\\begin{tabular' in l]
            self.end_table_indices = [lines.index(l) + 1
                                      for l in lines if '\\end{tabular' in l]
            return [self.begin_table_indices, self.end_table_indices]
        except Exception as e:
            print(e)
            raise Exception(e)

    def extractTables(self, saveLocation='/'):
        #assert self.check_if_valid() == True
        print('Running {}'.format(self.name))
        tableIndicies = self.find_all_table_indices()
        with open(self.input_file) as f:
            for x in range(0, len(tableIndicies[0])):
                lines = []
                for position, line in enumerate(f):
                    if position in range(tableIndicies[0][x], tableIndicies[1][x]):
                        lines.append(line)
                with open(saveLocation + self.input_file.split('.')[0].split('/')[-1] + '.txt', 'w') as t:
                    for line in lines:
                        t.write('%s\n' % line)
