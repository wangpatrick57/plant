#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

def get_low_k_index_path(gtag, k):
    return get_data_path(f'low_k/{gtag}-{k}.out')

def get_low_k_seeds_path(gtag1, gtag2, k):
    return get_data_path(f'low_k/{gtag1}-{gtag2}-{k}.seeds')

def run_seeding_low_k(gtag1, gtag2, k, overwrite=False):
    seeds_path = get_low_k_seeds_path(gtag1, gtag2, k)
    g1_index_path = get_low_k_index_path(gtag1, k)
    g2_index_path = get_low_k_index_path(gtag2, k)
    g1_graph_path = get_graph_path(gtag1)
    g2_graph_path = get_graph_path(gtag2)
    g1_to_g2_orthologs = get_g1_to_g2_orthologs(gtag1, gtag2)

    if overwrite or not file_exists(seeds_path):
        seeds = raw_full_low_param_run(g1_index_path, g1_graph_path, g2_index_path, g2_graph_path, g1_to_g2_orthologs, k=k)
        seeds_str = seeds_to_str(seeds)
        write_to_file(seeds_str, seeds_path)
    else:
        print(f'using old seeds file for {gtag1}-{gtag2}', file=sys.stderr)

if __name__ == '__main__':
    run_seeding_low_k(sys.argv[1], sys.argv[2], int(sys.argv[3]))
