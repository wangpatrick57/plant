#!/bin/python3
import os
import re
from collections import namedtuple
from seeding_algorithm_core import SeedingAlgorithmSettings

def get_tmp_path(path):
    return f'/tmp/{path}'

def get_seeds_path(gtag1, gtag2, algo='stairs', settings=SeedingAlgorithmSettings(), do_patch=True):
    return get_data_path(f'seeds/{gtag1}-{gtag2}_{algo}_mi{settings.max_indices}_st{settings.sims_threshold}_patch{do_patch}.seeds')

def get_plant_path(path):
    assert 'PLANT_REPO_DIR' in os.environ and os.environ['PLANT_REPO_DIR'] != '', 'PLANT_REPO_DIR is not set'
    return f'{os.environ["PLANT_REPO_DIR"]}/{path}'

def get_blant_path(path):
    assert 'BLANT_DIR' in os.environ and os.environ['BLANT_DIR'] != '', 'BLANT_DIR is not set'
    return f'{os.environ["BLANT_DIR"]}/{path}'

def get_wayne_path(path):
    return get_data_path(f'wayne/{path}')

def file_exists(path):
    exists = os.path.exists(path)

    if exists:
        with open(path, 'r') as f:
            line = f.readline()
            is_empty = line == ''
            return not is_empty

        raise Exception
    else:
            return False

def get_num_lines(path):
    with open(path, 'r') as f:
        return len(f.readlines())

def get_data_path(data_path):
    return f'{os.environ["PLANT_DATA_DIR"]}/{data_path}'

def remove_extension(path):
    return '.'.join(path.split('.')[:-1])

def read_in_m2m(m2m_path, ignore_invalid_lines=False):
    m2m_pairs = []

    with open(m2m_path, 'r') as f:
        for line in f:
            splitted = re.split('\s', line.strip())

            if len(splitted) != 2:
                if ignore_invalid_lines:
                    continue
                else:
                    raise AssertionError(f'The line "{line.encode("unicode_escape")}" is invalid')

            node1, node2 = splitted
            m2m_pairs.append((node1, node2))

    return m2m_pairs

def read_in_alignment(alignment_path, adj_set1, adj_set2):
    from analysis_helpers import assert_is_clean_alignment
    alignment = read_in_m2m(alignment_path)
    assert_is_clean_alignment(alignment, adj_set1, adj_set2)
    return alignment

def get_results_path(name):
    return get_data_path(f'results/{name}_results.txt')

SNSResult = namedtuple('SNSResult', ['size', 'nc', 's3'])

def read_in_pair_sns_results(results_path):
    results = dict()
    
    with open(results_path) as f:
        for line in f:
            pair, size, nc, s3 = re.split('\s', line.strip())
            size = int(size)
            nc = float(nc)
            s3 = float(s3)
            results[pair] = SNSResult(size, nc, s3)

    return results

def alignment_to_str(alignment):
    return '\n'.join(['\t'.join(pair) for pair in alignment])

def alignments_to_str(alignments):
    s = ''

    for alignment in alignments:
        s += 'NEW ALIGNMENT\n'

        for pair in alignment:
            s += ' '.join(pair) + '\n'

    return s

def write_perfect_orthologs_to_file(gtag, path):
    from graph_helpers import read_in_nodes
    
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
    os.makedirs(os.path.dirname(fpath), exist_ok=True)

    with open(fpath, 'w') as f:
        f.write(s)
        
if __name__ == '__main__':
    print(file_exists(sys.argv[1]))
