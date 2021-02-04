import os

DIR = os.getcwd()+'/tests/tables/'

tables = sorted([DIR + filename for filename in os.listdir(DIR)])

# print(tables)

with open(tables[1]) as f:
    lines = f.readlines()

    for line in lines:
        if "{table" in line:
            print(line)
