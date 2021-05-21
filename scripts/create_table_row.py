import sys
from graph_helpers import *
from collections import defaultdict

pk = int(sys.argv[1])
species1 = sys.argv[2]
species2 = sys.argv[3]
seeds_file = open(sys.argv[4], 'r')
mode = sys.argv[5] if len(sys.argv) >= 6 else 'ROW'
ORTHO_FILE = open(f'/home/wayne/src/bionets/SANA/Jurisica/IID/Orthologs.Uniprot.tsv', 'r')

def get_full_match_distr_str(full_match_distr):
    perfect = full_match_distr[10]
    good = sum([full_match_distr[i] for i in range(7, 10)])
    moderate = sum([full_match_distr[i] for i in range(4, 7)])
    bad = sum([full_match_distr[i] for i in range(1, 4)])
    none = full_match_distr[0]
    
    if mode == 'ROW':
        return f'{perfect} {good} {moderate} {bad} {none}'
    elif mode == 'SUMMARY':
        total = sum(full_match_distr.values())

        if total == 0:
            return '0'
        else:
            return f'{perfect * 100 / total:.2f}'

def main():
    s1_to_s2 = get_si_to_sj(species1, species2, ORTHO_FILE);
    full_match_distr = defaultdict(int)

    for line in seeds_file:
        gid, s1_index_str, s2_index_str = line.strip().split(' ')
        s1_index = s1_index_str.split(',')
        s2_index = s2_index_str.split(',')
        num_missing = get_num_missing(s1_index, s2_index, s1_to_s2);
        full_match_distr[pk - num_missing] += 1

    print(get_full_match_distr_str(full_match_distr))

if __name__ == '__main__':
    main()
