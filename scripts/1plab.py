#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys
import os

def remove_self_edges(graph_path):
    tel = []
    
    with open(graph_path, 'r') as graph_file:
        num_edges = 0

        for i, line in enumerate(graph_file):
            node1, node2, time = re.split('[\s\t]', line.strip())

            if node1 == node2:
                continue
            
            time = int(time)
            tel.append((node1, node2, time))
            num_edges += 1

    with open(graph_path, 'w') as graph_file:
        write_to_file(tel_to_str(tel), graph_path)

for gtag in ['sxso', 'math', 'super', 'ubuntu']:
    remove_self_edges(get_tgraph_path(gtag))
