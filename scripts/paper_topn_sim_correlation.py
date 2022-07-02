#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

pairs_str = '''cat-cow
cat-dog
cat-guineapig
cat-horse
cat-human
cat-mouse
cat-pig
cat-rabbit
cat-rat
cat-sheep
cow-dog
cow-guineapig
cow-horse
cow-human
cow-mouse
cow-pig
cow-rabbit
cow-rat
cow-sheep
dog-guineapig
dog-horse
dog-human
dog-mouse
dog-pig
dog-rabbit
dog-rat
dog-sheep
guineapig-horse
guineapig-human
guineapig-mouse
guineapig-pig
guineapig-rabbit
guineapig-rat
guineapig-sheep
horse-human
horse-mouse
horse-pig
horse-rabbit
horse-rat
horse-sheep
human-mouse
human-pig
human-rabbit
human-rat
human-sheep
mouse-pig
mouse-rabbit
mouse-rat
mouse-sheep
pig-rabbit
pig-rat
pig-sheep
rabbit-rat
rabbit-sheep
rat-sheep'''
n = 5

for pair_str in pairs_str.split('\n'):
    gtag1, gtag2 = pair_str.split('-')
    num_matching, num_total = analyze_top_nodes_similarity(gtag1, gtag2, n)
    print(num_matching)

