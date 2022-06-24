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
    gtag_dir['c28'] = ['facebook', 'facebook_5v1', 'facebook_5v2', 'facebook_5v3', 'facebook_5v4', 'facebook_5v5']
    gtag_dir['c29'] = ['git', 'git_5v1', 'git_5v2', 'git_5v3', 'git_5v4', 'git_5v5']
    gtag_dir['c30'] = ['astroph', 'astroph_5v1', 'astroph_5v2', 'astroph_5v3', 'astroph_5v4', 'astroph_5v5']
    gtag_dir['c31'] = ['cond', 'cond_5v1', 'cond_5v2', 'cond_5v3', 'cond_5v4', 'cond_5v5']
    gtag_dir['c32'] = ['hepph', 'hepph_5v1', 'hepph_5v2', 'hepph_5v3', 'hepph_5v4', 'hepph_5v5']
    gtag_dir['c33'] = ['hepth', 'hepth_5v1', 'hepth_5v2', 'hepth_5v3', 'hepth_5v4', 'hepth_5v5']
    gtag_dir['c34'] = ['enron', 'enron_5v1', 'enron_5v2', 'enron_5v3', 'enron_5v4', 'enron_5v5']
    gtag_dir['c35'] = ['caida', 'caida_5v1', 'caida_5v2', 'caida_5v3', 'caida_5v4', 'caida_5v5']
    gtag_dir['c36'] = ['oreg2', 'oreg2_5v1', 'oreg2_5v2', 'oreg2_5v3', 'oreg2_5v4', 'oreg2_5v5']
    gtag_dir['c37'] = ['gnu24', 'gnu24_5v1', 'gnu24_5v2', 'gnu24_5v3', 'gnu24_5v4', 'gnu24_5v5']
    gtag_dir['c38'] = ['gnu30', 'gnu30_5v1', 'gnu30_5v2', 'gnu30_5v3', 'gnu30_5v4', 'gnu30_5v5']
    gtag_dir['c99'] = ['math_std0', 'math_std05'] # all done already
    gtag_dir['c39'] = ['reddit_std0', 'reddit_std05']
    gtag_dir['c99'] = ['syeast0', 'syeast05', 'syeast10', 'syeast15', 'syeast20', 'syeast25'] # all done already
    gtag_dir['c40'] = get_all_iid_mammals()

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
