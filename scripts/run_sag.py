#!/bin/python3
import sys
from all_helpers import *

def run_sag(gtag1, gtag2, max_indices, sims_threshold):
    k_max = 1000
    # auto_k = (10000, 0.01)
    auto_k = None

    algo = 'stairs'
    overwrite = True
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    sag_alignment_path = get_sag_alignment_path(gtag1, gtag2, k_max=k_max, auto_k=auto_k)
    time_path = '.'.join(sag_alignment_path.split('.')[:-1]) + '.time'
    pair = f'{gtag1}-{gtag2}'

    if not overwrite and os.path.exists(sag_alignment_path):
        alignment = read_in_alignment(sag_alignment_path, adj_set1, adj_set2)
    else:
        start_time = time.time()
        seeds, _, _ = simplified_run_with_metrics(gtag1, gtag2, settings=SeedingAlgorithmSettings(max_indices=max_indices, sims_threshold=sims_threshold))
        blocks = seeds_to_blocks(seeds)
        sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2, p_func=ALWAYS_P_FUNC, s3_threshold=1)
        alignment = sagrow.run(k_max=k_max, auto_k=auto_k, silent=False)
        alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
        end_time = time.time()
        write_to_file(alignment_to_str(alignment), sag_alignment_path)
        write_to_file(f'{end_time - start_time}', time_path)

    size = len(alignment)
    nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
    s3 = get_s3(alignment, adj_set1, adj_set2)
    return (alignment, size, nc, s3)

def get_sag_alignment_path(gtag1, gtag2, k_max=None, auto_k=None):
    assert not (k_max == None and auto_k == None)
    assert not (k_max != None and auto_k != None)
    
    if auto_k != None:
        return get_data_path(f'simanneal/{gtag1}-{gtag2}-w{auto_k[0]}-p{int(auto_k[1] * 100)}.align')
    elif k_max != None:
        return get_data_path(f'simanneal/{gtag1}-{gtag2}-k{k_max}.align')
    else:
        raise AssertionError()

if __name__ == '__main__':
    from seeding_algorithm_core import SeedingAlgorithmSettings
    
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    max_indices = int(sys.argv[3])
    sims_threshold = float(sys.argv[4])
    
    print(run_sag(gtag1, gtag2, max_indices, sims_threshold))
