#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

def get_low_k_index_path(gtag, k):
    return get_data_path(f'low_k/{gtag}-{k}.out')

def get_low_k_seeds_path(gtag1, gtag2, k):
    return get_data_path(f'low_k/{gtag1}-{gtag2}-{k}.seeds')

def run_blant_low_k(gtag, k, overwrite=False):
    lDEG = 2
    alph = True
    algo = 'stairs'
    assert alph != None # alph can't be None because we need a different .sh script for that
    assert algo != None # just cuz I was too lazy to make a run command that used the default algo and also allowed a custom k
    graph_path = get_graph_path(gtag)
    out_path = get_low_k_index_path(gtag, k)

    if overwrite or not file_exists(out_path):
        settings = f'{algo} {graph_path} {lDEG} {bool_conv(alph)} {out_path} {k}'
        cmd = f'run_blant_low_k.sh {settings}'
        p = subprocess.Popen(cmd.split())
    else:
        p = None
        print(f'using old index file for {gtag}', file=sys.stderr)

    return p, out_path

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
