#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import os

for gtag in get_paper_all_gtags(False):
    idx_path = get_index_path(gtag)
    n = gtag_to_n(gtag)
    idx_size = os.path.getsize(idx_path)
    print(gtag, n, idx_size / 1_000_000)
