#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import random

ort = get_g1_to_g2_orthologs('mouse', 'rat')
s = ''

for mouse, rat in ort.items():
    num = random.uniform(0.6, 1.0)
    s += f'{mouse}\t{rat}\t{num}\n'

write_to_file(s, get_data_path(f'mcl/fake_ort/mouse-rat-k4-n15000-truerand.ort'))
