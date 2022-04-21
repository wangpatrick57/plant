#!/bin/python3
from species_helpers import *

def gen_dm_comm(species1, species2):
    return f'run_dm.sh {species1} {species2}'

all_species_pairs = get_all_species_pairs()

print(len(all_species_pairs))

for i, pair in enumerate(all_species_pairs):
    if i < 27:
        print(gen_dm_comm(pair[0], pair[1]))
    
