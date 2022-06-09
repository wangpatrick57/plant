#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

def gen_adv_graphs(gtags, advis, overwrite=False):
    for gtag in gtags:
        for advi in advis:
            adv_el = get_adversarial_el(gtag, advi)
            path = get_adv_graph_path(gtag, advi)

            if overwrite or not file_exists(path):
                write_el_to_file(adv_el, path)

def print_adv_report(gtags, advis):
    gen_adv_graphs(gtags, advis)
    gen_all_indexes(gtags, 'bno', 1)

if __name__ == '__main__':
    gen_adv_graphs(['syeast0', 'syeast05'], [0])
