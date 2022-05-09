#!/pkg/python/3.7.4/bin/python3
import sys
from graph_helpers import *

path = sys.argv[1]

with open(path, 'r') as btc_file:
    el = []

    for line in btc_file:
        source, target, rating, time = line.strip().split(',')
        el.append((source, target))

    print_el(el)
