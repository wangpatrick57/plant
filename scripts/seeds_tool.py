#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

LDEG = 3
syeasts = get_all_syeasts()
syeast0 = syeasts[0]

for other in syeasts[1:]:
    gtag1 = syeast0
    gtag2 = other
    run_info = get_gtag_run_info(gtag1, gtag2, g1_alph=True, g2_alph=True, algo='bno', lDEG=LDEG)
    out_path = get_data_path(f'syeast/{gtag1}-{gtag2}-lDEG{LDEG}-seeds.txt')
    seeds, seed_metrics, extr_metrics = low_param_one_run(*run_info)
    seeds_str = seeds_to_str(seeds)
    write_to_file(seeds_str, out_path)
    print(f'done with {gtag1}-{gtag2}, {seed_metrics}, {extr_metrics}')
