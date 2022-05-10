#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *

def write_seeds_to_files(orthoseeds, allseeds, file_path_func):
    write_to_file_helper(orthoseeds, file_path_func('orthoseeds'))
    write_to_file_helper(allseeds, file_path_func('allseeds'))

def write_to_file_helper(seeds, file_path):
    outfile = open(file_path, 'w')

    for gid, index1, index2 in seeds:
        index1_str = ','.join(index1)
        index2_str = ','.join(index2)
        outfile.write(f'{gid}\t{index1_str}\t{index2_str}\n')

    outfile.close()

def write_el_to_file(el, file_path):
    el = clean_el(el)
    outfile = open(file_path, 'w')

    for node1, node2 in el:
        outfile.write(f'{node1}\t{node2}\n')

    outfile.close()
        
if __name__ == '__main__':
    write_to_file_helper([(10, ('1', '2'), ('3', '4')), (30, ('1', '5'), ('7', '3'))], 'temp.txt')
