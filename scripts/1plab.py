#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

seeds = [
    (1, ('a', 'z'), ('a', 'b')),
    (2, ('a', 'b', 'c'), ('a', 'b', 'c')),
    (1, ('c'), ('c')),
    (2, ('c'), ('c'))
]
g1_to_g2_ort = SelfOrthos()
print(get_seed_nc(seeds, g1_to_g2_ort))
