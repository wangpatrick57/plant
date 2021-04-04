import sys
import random
import re

graph_file = open(sys.argv[1], 'r')
graph_lines = []

for line in graph_file:
    node1, node2 = re.split('\s+', line.strip())
    graph_lines.append((node1, node2))

random.shuffle(graph_lines)

for node1, node2 in graph_lines:
    if random.uniform(0, 1) < 0.5:
        print(f'{node1}\t{node2}')
    else:
        print(f'{node2}\t{node1}')
