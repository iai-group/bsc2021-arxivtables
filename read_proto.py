import proto.tables_pb2 as table_proto
paper = table_proto.Paper()

with open('db/arxiv_papers/21/05/2105.06863', 'rb') as f:
  paper.ParseFromString(f.read())

print(paper)