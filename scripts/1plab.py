#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

#r = range(3, 9)
r = [5]

for k in r:
    canon_list, orbit_map = read_in_canon_list_and_orbit_map(k)
    print_el(get_bv_el_with_blantitl_orbit_nodes(254, canon_list, orbit_map))
