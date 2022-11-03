#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys
import os

canon_list = read_in_canon_list(int(sys.argv[1]))
bvs = get_connected_bvs(canon_list)
print(len(bvs))
