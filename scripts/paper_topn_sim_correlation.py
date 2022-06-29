#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

n = 10

for gtag1, gtag2 in get_paper_all_pairs():
    num_matching, num_total = analyze_top_nodes_similarity(gtag1, gtag2, n)
    print(num_matching)

