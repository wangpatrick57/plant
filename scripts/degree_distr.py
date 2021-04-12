import sys
import re
from collections import defaultdict

def print_degree_distr(graph):
    degree_distr = defaultdict(int)

    for adj in graph.values():
        degree_distr[len(adj)] += 1

    print('\n'.join([f'{degree} {count}' for degree, count in degree_distr.items()]))

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
    print_degree_distr(graph)
