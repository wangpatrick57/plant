#!/pkg/python/3.7.4/bin/python3
from collections import defaultdict
from all_helpers import *

k = 6
spec = 'sy0'
cname = f'test_c_{spec}_k{k}l2.out'
pyname = f'test_py_{spec}_k{k}l2.out'

cgraphlets = set()
pygraphlets = set()

with open(cname, 'r') as cf:
    for line in cf:
        splitted = line.strip().split()
        nodes = tuple(sorted(splitted[1:]))
        cgraphlets.add(nodes)

with open(pyname, 'r') as pyf:
    for line in pyf:
        splitted = line.strip().split()
        nodes = tuple(sorted(splitted))
        pygraphlets.add(nodes)

in_c_not_py = 0
in_py_not_c = 0

for cgraphlet in list(cgraphlets):
    if cgraphlet not in pygraphlets:
        in_c_not_py += 1

for pygraphlet in list(pygraphlets):
    if pygraphlet not in cgraphlets:
        in_py_not_c += 1
        print(pygraphlet)

print(in_c_not_py, in_py_not_c)
