#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

for k in range(1, 9):
    print(k)
    print(get_num_orbits(k))
    print(get_num_orbits_cum(k))
    print()
