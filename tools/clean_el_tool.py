#!/bin/python3
import sys
from file_helpers import *
from graph_helpers import *

gtag = sys.argv[1]
path = get_graph_path(gtag)
el = read_in_el(path)
el = clean_el(el)
num_lines = get_num_lines(path)
print(f'{path} before: {num_lines}')
write_el_to_file(el, path)
num_lines = get_num_lines(path)
print(f'{path} after: {num_lines}')
