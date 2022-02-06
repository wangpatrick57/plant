#!/bin/python3
from full_algorithm_helpers import *

# run algorithm
k = 8
species1 = 'mouse'
species2 = 'rat'
orbits = list(range(15))
orbits_str = 'allorbs'
max_indices = 50
sims_threshold = 0.79

orthoseeds, all_seeds = full_run_algorithm_basic_seeds(k, species1, species2, orbits, max_indices, sims_threshold, print_progress=True)
print(f'{len(orthoseeds)} / {len(all_seeds)}')

# write to files
orthoseeds_out_file = open(f'/home/wangph1/plant/data/seeding_cached_data/paper_final/{species1}-{species2}-final-{orbits_str}-max{max_indices}-thresh{sims_threshold}-orthoseeds.out', 'w')
allseeds_out_file = open(f'/home/wangph1/plant/data/seeding_cached_data/paper_final/{species1}-{species2}-final-{orbits_str}-max{max_indices}-thresh{sims_threshold}-allseeds.out', 'w')

for graphletid, index1, index2 in orthoseeds:
    index1_str = ','.join(index1)
    index2_str = ','.join(index2)
    orthoseeds_out_file.write(f'{graphletid}\t{index1_str}\t{index2_str}\n')

for graphletid, index1, index2 in all_seeds:
    index1_str = ','.join(index1)
    index2_str = ','.join(index2)
    allseeds_out_file.write(f'{graphletid}\t{index1_str}\t{index2_str}\n')

orthoseeds_out_file.close()
allseeds_out_file.close()
