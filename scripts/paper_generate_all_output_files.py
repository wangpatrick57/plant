#!/bin/python3
import sys
from paper_final_algorithm import *
from graph_helpers import *

def write_to_output_file(species1, species2, pairs, output_type):
    filename = f'{output_type}-{species1}-{species2}.out'
    out_file = open(f'/home/wangph1/plant/data/seeding_cached_data/paper_final/{filename}', 'w')
    
    for node1, node2 in pairs:
        out_file.write(f'{node1}\t{node2}\n')

    out_file.close()

def write_to_output_files(species1, species2, orthopairs, outpairs):
    write_to_output_file(species1, species2, orthopairs, 'orthopairs')
    write_to_output_file(species1, species2, outpairs, 'outpairs')

if __name__ == '__main__':
    all_iid_mammals = get_all_iid_mammals()

    for i in range(len(all_iid_mammals)):
        species1 = all_iid_mammals[i]

        for j in range(i, len(all_iid_mammals)):
            species2 = all_iid_mammals[j]
            orthopairs, outpairs = get_final_answer(species1, species2)
            write_to_output_files(species1, species2, orthopairs, outpairs)
            print(f'done with {species1}-{species2}')
