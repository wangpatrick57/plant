#!/bin/python3
from time import time
from paper_final_algorithm import *
import sys
from species_helpers import *
from validation_helpers import *

species1 = sys.argv[1]

results = []

print(get_all_species())

for species2 in get_all_species():
    if species1 != species2:
        start_time = time()
        orthopairs, allpairs = get_final_answer_patch_pairs(species1, species2, print_progress=False)
        results.append((orthopairs, allpairs))
        end_time = time()
        print(f'{species1}-{species2}: {len(orthopairs)} / {len(allpairs)}, {end_time - start_time} seconds')

for result in results:
    print(f'{len(orthopairs)}\t{len(allpairs)}')
