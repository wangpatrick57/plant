#!/bin/python3
import sys
import re
from collections import defaultdict

def get_degree_distr(graph, do_print=False):
    return get_sub_degree_distr(graph, graph.keys(), do_print=do_print)

def get_sub_degree_distr(graph, nodes_to_count, do_print=False):
    degree_distr = defaultdict(int)

    for node in nodes_to_count:
        degree_distr[len(graph[node])] += 1

    if do_print:
        print('\n'.join([f'{degree} {count}' for degree, count in sorted(degree_distr.items())]))

    return degree_distr

def read_in_graph(path):
    with open(path, 'r') as graph_file:
        graph = dict()

        for line in graph_file:
            node1, node2 = re.split('\s', line.strip())

            if node1 not in graph:
                graph[node1] = list()

            if node2 not in graph:
                graph[node2] = list()
            
            graph[node1].append(node2)
            graph[node2].append(node1)

    return graph

if __name__ == '__main__':
    path = sys.argv[1]
    graph = read_in_graph(path)
    get_degree_distr(graph, do_print=True)
