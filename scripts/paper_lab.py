#!/bin/python3
import sys
from full_algorithm_helpers import *

orthopairs, all_pairs = full_run_algorithm_basic(8, 'mouse', 'rat', [0], 55, 0.78, print_progress=False)
print('\n'.join([f'{node1}\t{node2}' for node1, node2 in orthopairs]))
print('\n'.join([f'{node1}\t{node2}' for node1, node2 in all_pairs]), file=sys.stderr)
