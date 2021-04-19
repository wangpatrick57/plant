import sys
from collections import defaultdict
import re

index_file = open(sys.argv[1], 'r')
graphlet_distr = defaultdict(int)

for line in index_file:
    graphlet_id = re.split('\s', line.strip())[0]
    graphlet_distr[graphlet_id] += 1

for graphlet_id in sorted(graphlet_distr.keys(), key=(lambda data: graphlet_distr[data]), reverse=True):
    print(f'{graphlet_id} {graphlet_distr[graphlet_id]}')
    
