import sys
from collections import defaultdict

orthoseeds_file = sys.argv[1]
s1_nodes = set()
s2_nodes = set()
graphlet_distr = defaultdict(int)
total_nodes_num = 0

for line in open(orthoseeds_file, 'r'):
    graphlet_id, s1_index_str, s2_index_str = line.strip().split(' ')
    graphlet_id = graphlet_id
    s1_index = s1_index_str.split(',')
    s2_index = s2_index_str.split(',')

    for s1_node in s1_index:
        s1_nodes.add(s1_node)

    for s2_node in s2_index:
        s2_nodes.add(s2_node)

    graphlet_distr[graphlet_id] += 1

sorted_graphlet_distr = sorted(list(graphlet_distr.items()), key = (lambda item : item[1]))
print(f'graphlet distribution', file=sys.stderr)
print('\n'.join(f'{id} {count}' for id, count in sorted_graphlet_distr), file=sys.stderr)
print(f'species1 covers {len(s1_nodes)} nodes', file=sys.stderr)
print(f'species2 covers {len(s2_nodes)} nodes', file=sys.stderr)
print('\n'.join(s1_nodes))
