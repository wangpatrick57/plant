#!/bin/python3
from seeding_algorithm_core import *
from blant_cache_helpers import *

k = 8
species1="mouse"
species2="rat"
s1_index_path = get_index_path(species1)
s2_index_path = get_index_path(species2)
s1_indexed_indices = get_indexed_indices(s1_index_path, k)
s2_indexed_indices = get_indexed_indices(s2_index_path, k)

for max_indices in range(10000, 1000000, 10000):
    settings = SeedingAlgorithmSettings(max_indices=max_indices)
    estimated_pairs = estimate_total_pairs_to_process(s1_indexed_indices, s2_indexed_indices, settings)
    print(f'{max_indices}\t{estimated_pairs}')
