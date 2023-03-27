#!/bin/python3
import sys
from all_helpers import *
import argparse

# "sag" stands for Simulated Annealing Grow

def run_sag(gtag1, gtag2, max_indices, sims_threshold, overwrite=False):
    k_max = 5000
    # auto_k = (10000, 0.01)
    auto_k = None

    algo = 'stairs'
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
        sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2, p_func=ALWAYS_P_FUNC, s3_threshold=0.95)
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

# THE RUN_SAG.PY FILE OVERWRITES, BUT THE PAPER_ALL_* FILES THAT CALL RUN_SAG DON'T OVERWRITE
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='run_sag.py', description='Run the simulated annealing algorithm (Algorithm 3 in the paper)')
    parser.add_argument('gtag1', help='The graph tag (gtag) of the first graph')
    parser.add_argument('gtag2', help='The graph tag (gtag) of the second graph')
    parser.add_argument('-m', '--max-indices', type=int, default=1, help='The max_indices parameter of the seeds file to be used')
    parser.add_argument('-s', '--sims-threshold', type=float, default=-0.95, help='The sims_threshold parameter of the seeds file to be used')
    args = parser.parse_args()
    print(run_sag(args.gtag1, args.gtag2, args.max_indices, args.sims_threshold, overwrite=True))
