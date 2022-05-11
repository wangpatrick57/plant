#!/pkg/python/3.7.4/bin/python3
import sys
from full_algorithm_helpers import *

def gen_blant_commands(bases, adds, start_machine):
    bases = ['alpha', 'reddit', 'college', 'ubuntu']
    adds = ['0', '1', '2', '3']
    machine = start_machine

    for base in bases:
        print()
        print(f'ssh wangph1@circinus-{machine}.ics.uci.edu')

        for add in adds:
            snap = f'{base}{add}'
            print(f'run_blant_default.sh ~/plant/networks/snap/{snap}.el ~/plant/data/seeding_cached_data/blant_out/p0-o0-{snap}-lDEG2.out')

        machine += 1

def basic_sweep_base(base, line=None, pair=None):
    if line == pair == None or (line != None and pair != None):
        raise AssertionError('either line or pair must be defined, but not both')

    if line:
        compare = []

        for e in line[1:]:
            compare.append((line[0], e))
    elif pair:
        compare = pair

    for add1, add2 in compare:
        snap1 = f'{base}{add1}'
        snap2 = f'{base}{add2}'
        orthopairs, node_pairs = low_param_full_patch_results(*get_snap_run_info(snap1, snap2))
        print(f'{snap1} vs {snap2}')
        print(f'BLANT: {len(orthopairs)} / {len(node_pairs)}')

if __name__ == '__main__':
    base = 'college'
    line = ['1', '2', '3']
    basic_sweep_base(base, line)
