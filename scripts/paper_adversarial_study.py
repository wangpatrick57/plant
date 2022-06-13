#!/pkg/python/3.7.4/bin/python3
import sys
from all_helpers import *

def gen_adv_graphs(gtags, advis, overwrite=False):
    for gtag in gtags:
        for advi in advis:
            adv_el = get_adversarial_el(gtag, advi)
            path = get_adv_graph_path(get_adv_gtag(gtag, advi))

            if overwrite or not file_exists(path):
                write_el_to_file(adv_el, path)

def print_adv_report_line(gtag, advis, include_base):
    gen_adv_graphs([gtag], advis)
    adv_gtags = []

    if include_base:
        adv_gtags.append(gtag)
    
    for advi in advis:
        adv_gtags.append(get_adv_gtag(gtag, advi))

    algo = 'bnocpy1'
    lDEG = 2

    gen_all_indexes(adv_gtags, algo, lDEG)
    gtag1 = gtag
    extr_vols = []
    extr_ncs = []

    for gtag2 in adv_gtags:
        run_info = get_gtag_run_info(gtag1, gtag2, algo=algo, lDEG=lDEG)
        _, _, (extr_vol, extr_nc) = low_param_one_run(*run_info)
        extr_vols.append(extr_vol)
        extr_ncs.append(extr_nc)
        print(f'done with {gtag1}, {gtag2}', file=sys.stderr)

    print(gtag + '\t' + '\t'.join([str(vol) for vol in extr_vols]))
    print(gtag + '\t' + '\t'.join([str(nc) for nc in extr_ncs]))

if __name__ == '__main__':
    gtag = sys.argv[1]
    advis = [0, 1, 2, 3, 5, 8, 11, 15]
    print_adv_report_line(gtag, advis, True)
