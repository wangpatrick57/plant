#!/bin/python3
from all_helpers import *

for gtag in get_paper_all_gtags(False):
    idx_path = get_index_path(gtag)
    n = gtag_to_n(gtag)
    _, idx_time = extract_index_metrics(idx_path)
    print(gtag, n, idx_time)
