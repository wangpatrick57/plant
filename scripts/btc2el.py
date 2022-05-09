#!/pkg/python/3.7.4/bin/python3
import sys
from graph_helpers import *

is_tel = True
path = sys.argv[1]

with open(path, 'r') as btc_file:
    xel = []

    for line in btc_file:
        source, target, rating, time = line.strip().split(',')
        edge = [source, target]

        if is_tel:
            edge.append(str(int(float(time))))

        edge = tuple(edge)
        xel.append(edge)

    print_xel(xel)
