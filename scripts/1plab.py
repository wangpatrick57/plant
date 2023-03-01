#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

if __name__ == '__main__':
    from seeding_algorithm_core import SeedingAlgorithmSettings
    
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    seeds = raw_full_run(*get_gtag_run_info(gtag1, gtag2), settings=SeedingAlgorithmSettings(2, 0, 1))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    seed_metrics, extr_metrics = get_all_metrics(seeds, g1_to_g2_ort, gtag1=gtag1, gtag2=gtag2)
    print(len(seeds), seed_metrics)
