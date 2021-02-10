class TableExtractor:
    def __init__(self, input_file):
        self.name = 'TableExtractor for {}'.format(input_file)
        self.input_file = input_file
        self.begin_table_indices = []
        self.end_table_indices = []

    def check_if_valid(self):
        if self.input_file.endswith('.tex'):
            return True
        else:
            raise ValueError('"{}" is not a .tex file'.format(self.input_file))

    def find_all_table_indices(self):
        lines = []
        if self.check_if_valid():
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

    def extractTables(self):
        assert self.check_if_valid() == True
        tableIndicies = self.find_all_table_indices()
        with open(self.input_file) as f:
            for x in range(0, len(tableIndicies[0])):
                lines = []
                for position, line in enumerate(f):
                    if position in range(tableIndicies[0][x], tableIndicies[1][x]):
                        lines.append(line)
                with open('/home/david/repos/school/bsc2021-arxivtables/output/' + self.input_file.split('.')[0].split('/')[-1] + '.txt', 'w') as t:
                    for line in lines:
                        t.write('%s\n' % line)
