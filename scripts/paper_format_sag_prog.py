#!/bin/python3
import sys
from all_helpers import *

k_max_lists = []

for gtag1, gtag2 in get_paper_all_pairs():
    pair = (gtag1, gtag2)
    prog_path = get_data_path(f'simanneal/{gtag1}-{gtag2}-sag_progress.txt')
    k_max_list = []

    with open(prog_path) as f:
        for line in f:
            k, _, max_size = line.strip().split('\t')
            k = int(k)
            max_size = int(max_size)
            k_max_list.append((k, max_size))

    last_k = k_max_list[-1][0]

    if last_k != 99900:
        print(f'{prog_path} ends with k={last_k}', file=sys.stderr)
        
    k_max_lists.append(k_max_list)

for i in range(len(k_max_lists) - 1):
    assert len(k_max_lists[i]) == len(k_max_lists[i + 1])

for i in range(len(k_max_lists[0])):
    for k_max_list in k_max_lists:
        max_max = k_max_list[-1][1]
        curr_k = k_max_list[i][0]
        curr_max = k_max_list[i][1]
        curr_max_percent = curr_max / max_max * 100
        print(f'{curr_k}\t{curr_max_percent}\t\t', end='')

    print()
