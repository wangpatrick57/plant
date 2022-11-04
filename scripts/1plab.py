#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

gtag = sys.argv[1]
k = int(sys.argv[2])
nstr = sys.argv[3]
odv_dir = get_combined_odv_file(gtag, k, nstr)
print(odv_dir.get_odv(list(odv_dir.get_nodes())[0]))
