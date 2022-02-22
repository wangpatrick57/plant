#!/bin/python3
from full_algorithm_helpers import *

species1 = 'mouse'
species2 = 'rat'
orbits = [0]
sims_threshold = 0
max_indices = 1

orthoseeds, allseeds = full_get_seeds_results(8, species1, species2, orbits, max_indices, sims_threshold)

print(len(orthoseeds), len(allseeds))
