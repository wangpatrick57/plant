#!/pkg/python/3.7.4/bin/python3
import sys
from index_helpers import *

index1_path = get_index_path('syeast0', 0, 0, lDEG=2, alph=True)
index2_path = get_index_path('syeast0', 0, 0, lDEG=2, alph=False)
index1 = read_in_index(index1_path, 8)
index2 = read_in_index(index2_path, 8)
print(f'{index1_path} == {index2_path}?', index1 == index2)
