#!/pkg/python/3.7.4/bin/python3
import os
from graph_helpers import *

PLANT_DIR = '/home/wangph1/plant'

def file_exists(path):
    return os.path.exists(path)

def get_data_path(data_path):
    return f'{PLANT_DIR}/data/{data_path}'

def read_in_m2m(m2m_path):
    m2m_pairs = []

    with open(m2m_path, 'r') as f:
        for line in f:
            node1, node2 = line.strip().split('\t')
            m2m_pairs.append((node1, node2))

    return m2m_pairs

def read_in_slashes_m2m(m2m_path):
    m2m_pairs = []

    with open(m2m_path, 'r') as f:
        for cluster in f:
            for line in cluster.split('\t'):
                node1, node2 = line.split('/')
                m2m_pairs.append((node1, node2))

    return m2m_pairs

def write_perfect_orthologs_to_file(gtag, path):
    graph_path = get_graph_path(gtag)
    nodes = read_in_nodes(graph_path)
    mark = gtag_to_mark(gtag)

    with open(path, 'w') as f:
        for node in nodes:
            marked_node = f'{mark}_{node}'
            f.write(f'{node}\t{marked_node}\t1\n')

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

def write_to_file(s, fpath):
    with open(fpath, 'w') as f:
        f.write(s)
        
if __name__ == '__main__':
    out_path = get_data_path('mcl/fake_ort/syeast-syeast-perf.ort')
    write_perfect_orthologs_to_file('syeast0', out_path)
