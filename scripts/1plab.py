#!/pkg/python/3.7.4/bin/python3
import sys
from graph_helpers import *
from file_helpers import *

graph_path = sys.argv[1]
el = read_in_el(graph_path)
nxg = el_to_nxg(el)
print([len(ccs) for ccs in get_ccs_list(nxg)])
