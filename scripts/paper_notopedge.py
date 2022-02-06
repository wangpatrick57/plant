#!/bin/python3
from seeding_algorithm_core import *
from blant_cache_helpers import *
from odv_helpers import *
from ortholog_helpers import *
from file_helpers import *

# setup
k = 8
species1 = 'mouse'
species2 = 'rat'
s1_index_path = get_index_path(species1)
s2_index_path = get_index_path(species2)
s1_notopedge_index_path = get_notopedge_index_path(species1)
s2_notopedge_index_path = get_notopedge_index_path(species2)
s1_odv_path = get_odv_file_path(species1)
s2_odv_path = get_odv_file_path(species2)
settings = SeedingAlgorithmSettings(max_indices=15, sims_threshold=0.79, speedup=1)
s1_to_s2_orthologs = get_s1_to_s2_orthologs(species1, species2)

# both normal
allseeds = find_seeds(k, species1, species2, s1_index_path, s2_index_path, s1_odv_path, s2_odv_path, settings, print_progress=False)
orthoseeds = get_orthoseeds_list(allseeds, s1_to_s2_orthologs)
print(f'both normal: {len(orthoseeds)} / {len(allseeds)}')
write_seeds_to_files(orthoseeds, allseeds, (lambda seed_type : f'/home/wangph1/plant/data/seeding_cached_data/paper_final/mouse-rat-max15-thresh0.79-{seed_type}.out'))

# mouse notopedge, rat normal
allseeds = find_seeds(k, species1, species2, s1_notopedge_index_path, s2_index_path, s1_odv_path, s2_odv_path, settings, print_progress=False)
orthoseeds = get_orthoseeds_list(allseeds, s1_to_s2_orthologs)
print(f'mouse notopedge: {len(orthoseeds)} / {len(allseeds)}')

# mouse normal, rat notopedge
allseeds = find_seeds(k, species1, species2, s1_index_path, s2_notopedge_index_path, s1_odv_path, s2_odv_path, settings, print_progress=False)
orthoseeds = get_orthoseeds_list(allseeds, s1_to_s2_orthologs)
print(f'rat notopedge: {len(orthoseeds)} / {len(allseeds)}')

# both notopedge
allseeds = find_seeds(k, species1, species2, s1_notopedge_index_path, s2_notopedge_index_path, s1_odv_path, s2_odv_path, settings, print_progress=False)
orthoseeds = get_orthoseeds_list(allseeds, s1_to_s2_orthologs)
print(f'both notopedge: {len(orthoseeds)} / {len(allseeds)}')
