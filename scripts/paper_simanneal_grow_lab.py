#!/bin/python3
from all_helpers import *

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]
algo = sys.argv[3]
write_alignment = bool(int(sys.argv[4])) if len(sys.argv) > 4 else False
adj_set1 = read_in_adj_set(get_graph_path(gtag1))
adj_set2 = read_in_adj_set(get_graph_path(gtag2))
g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
seeds_path = get_seeds_path(gtag1, gtag2, algo=algo, prox=1, target_num_matching=1)
seeds = read_in_seeds(seeds_path)
blocks = seeds_to_blocks(seeds)
sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2, p_func=ALWAYS_P_FUNC, s3_threshold=1)
alignment = sagrow.run(1000)
print(f'generated raw alignment with {len(alignment)} nodes')
alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
print(f'generated clean alignment with {len(alignment)} nodes')
size = len(alignment)
nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
s3 = get_s3(alignment, adj_set1, adj_set2)
print(f'final: size={size}, nc={nc}, s3={s3}')

if write_alignment:
    write_to_file(alignment_to_str(alignment), f'alignment_n{size}.txt')
