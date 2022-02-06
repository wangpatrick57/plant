#!/bin/python3
from paper_final_algorithm import *
from s3_helpers import *
import sys

def get_all_species2s(species1, s3_manager):
    return list(s3_manager.s3_scores[species1].keys())

def get_all_species1s(s3_manager):
    return list(s3_manager.s3_scores.keys())

if __name__ == '__main__':
    s3_manager = S3Manager()
    s3_manager.add_all_s3_scores()
    print(get_all_species1s(s3_manager))
    species1 = sys.argv[1]

    for species2 in get_all_species2s(species1, s3_manager):
        orthopairs, all_pairs = get_final_answer(species1, species2)
        print(f'{species1}-{species2}', len(orthopairs), len(all_pairs))

    
