#!/bin/python3
from all_helpers import *

def get_blantitl_to_blantout_mapping(k):
    bvs = get_connected_bitvectors(k)
    
    for bv in bvs:
        # get orbits
        # generate el
        # run blant
        pass

print(get_connected_bitvectors(int(sys.argv[1])))
