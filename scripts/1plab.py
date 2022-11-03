#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

k = int(sys.argv[1])
orbit_counts = calc_orbit_counts_autogen_graphlets(k)
print(orbit_counts)
print(len(orbit_counts))
print(get_num_orbits_cum(k))

