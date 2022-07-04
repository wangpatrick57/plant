#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

# start = int(sys.argv[1])
# pairs = get_paper_all_pairs()[start:start + 18]
pairs = get_low_volume_pairs()
end = pairs.index(('math_s0', 'math_s3'))
pairs = pairs[:end]
algo = 'stairs'

for gtag1, gtag2 in pairs:
    seeds, seed_metrics, extr_metrics = low_param_one_run(*get_gtag_run_info(gtag1, gtag2, algo=algo))
    write_to_file(seeds_to_str(seeds), get_seeds_path(gtag1, gtag2))
    to_print = [f'{gtag1}-{gtag2}', len(seeds), seed_metrics[0], seed_metrics[2], extr_metrics[0], extr_metrics[1]]
    print('\t'.join([str(e) for e in to_print]))
