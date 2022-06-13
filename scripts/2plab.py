#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

advis = [0, 1, 2, 3, 5, 8, 11, 15]

for advi in advis:
    gtag = f'hepph'
    index_path = get_index_path(gtag, algo='bno')

    with open(index_path, 'r') as f:
        print(len(f.readlines()))
