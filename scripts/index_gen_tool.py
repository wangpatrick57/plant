#!/pkg/python/3.7.4/bin/python3
import sys
from all_helpers import *

LDEG = 2
ALGO = 'bno'

# problematic gtags:
#  * deezer stopped at 68% for some advs on circ32 but worked on circ16. deezer_10v1a stoped at 2% on circ27 many days later
#  * astroph stopped at 34% for all advs on both circ33 and circ17, but 10v1a worked on circ26 many days later?

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
    bgs = get_biogrid_acronyms()
    bgs = [f'bg{bg}' for bg in bgs]

    gtag_dir['c20'] = bgs[0:1]
    gtag_dir['c21'] = bgs[1:2]
    gtag_dir['c22'] = bgs[2:3]
    gtag_dir['c23'] = bgs[3:4]
    gtag_dir['c24'] = bgs[4:5]
    gtag_dir['c25'] = bgs[5:6]
    gtag_dir['c26'] = bgs[6:7]
    gtag_dir['c27'] = bgs[7:8]

    machine = sys.argv[1]
    gtags = gtag_dir[machine]
    print_gtags_status(gtags)
    cont = input('Continue? ')

    while cont != 'y':
        if cont == 'n' or cont == 'q':
            quit()
        else:
            cont = input('Continue? ')

    gen_all_indexes_sequential(gtags, algo=ALGO, lDEG=LDEG)
