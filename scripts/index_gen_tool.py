#!/pkg/python/3.7.4/bin/python3
import sys
from all_helpers import *

LDEG = 2
ALGO = 'bno'

# problematic gtags:
#  * deezer stopped at 68% for some advs on circ32 but worked on circ16
#  * astroph stopped at 34% for all advs on both circ33 and circ17

def print_gtags_status(gtags):
    gtags = gtag_dir[machine]

    for gtag in gtags:
        path = get_index_path(gtag, algo=ALGO, lDEG=LDEG)
        fname = path.split('/')[-1]

        if file_exists(path):
            print(f'  -- {fname} already exists --')
        else:
            print(f'will gen {fname}')

if __name__ == '__main__':
    gtag_dir = dict()
    gtag_dir['c26'] = ['human', 'mouse', 'rat', 'syeast0', 'syeast15', 'math_std0', 'math_std10']
    gtag_dir['c27'] = ['deezer_10v1a']
    gtag_dir['c9'] = ['astroph_10v1a']
    gtag_dir['c48'] = ['enron_10v1a', 'enron_10v1b', 'caida_10v1a']
    gtag_dir['c23'] = ['caida_10v1b', 'gnu24_10v1a', 'gnu24_10v1b']

    machine = sys.argv[1]
    gtags = gtag_dir[machine]
    print_gtags_status(gtags)
    cont = input('Continue? ')

    while cont != 'y':
        if cont == 'n' or cont == 'q':
            quit()
        else:
            cont = input('Continue? ')

    gen_all_indexes(gtags, algo=ALGO, lDEG=LDEG)
