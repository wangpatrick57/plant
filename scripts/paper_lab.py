#!/bin/python3
from seeding_algorithm_core import *
from ortholog_helpers import *

species1 = 'mouse'
species2 = 'human'

def get_path(species):
    return f'/home/wangph1/plant/data/seeding_cached_data/special_blant_out/p0-o0-hayes{species}-lDEG2.out'
    # return f'/home/wangph1/plant/data/seeding_cached_data/blant_out/p0-o0-{species}-lDEG2.out'

allseeds = find_seeds(8, species1, species2, get_path(species1), get_path(species2), settings=SeedingAlgorithmSettings(max_indices=50, sims_threshold=0.8), print_progress=True)
orthoseeds = get_orthoseeds_list(allseeds, get_s1_to_s2_orthologs(species1, species2))

print(f'{len(orthoseeds)} / {len(allseeds)}')
