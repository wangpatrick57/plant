#!/pkg/python/3.7.4/bin/python3
import sys
from index_helpers import *

index1_path = get_index_path('mouse', 0, 0, alph=None)
index2_path = '/home/wangph1/plant/data/seeding_cached_data/messy_blant_out/SHUF-p0-o0-mouse-lDEG2.out'
index1 = read_in_index(index1_path, 8)
index2 = read_in_index(index2_path, 8)
print(str(index1[7155][0]))
print(str(index2[7155][0]))
print(index1[7155][0] == index2[7155][0])
print(index1 == index2)
