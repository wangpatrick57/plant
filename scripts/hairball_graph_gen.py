import random
import re
from collections import defaultdict, deque
import json
import copy


# SETTINGS
CORE_INITIAL_SIZE = 400
FOLLICLE_COUNT = 9900
HAIR_COUNT = FOLLICLE_COUNT * 3


# FUNCTIONS
def print_degree_distr(graph):
    degree_distr = defaultdict(int)

    for adj in graph.values():
        degree_distr[len(adj)] += 1

    print('\n'.join([f'{degree} {count}' for degree, count in degree_distr.items()]))

def print_el(graph):
    el = set()

    for node, adj in graph.items():
        for adj_node in adj:
            min_node = min(node, adj_node)
            max_node = max(node, adj_node)
            el.add((min_node, max_node))

    for node1, node2 in el:
        print(f'{node1} {node2}')

def get_induced_subgraph(graph, nodes):
    induced_subgraph = dict()

    for node, adj in graph.items():
        if node in nodes:
            new_adj_list = [adj_node for adj_node in adj if adj_node in nodes]
            induced_subgraph[node] = new_adj_list

    return induced_subgraph

def find_largest_connected_component(graph):
    all_remaining_nodes = set(graph.keys())
    components = list()

    while len(all_remaining_nodes) > 0:
        bfs_deque = deque()
        bfs_deque.append(all_remaining_nodes.pop())
        curr_component_nodes = set()

        while len(bfs_deque) > 0:
            curr_node = bfs_deque.pop()
            curr_component_nodes.add(curr_node)

            for adj_node in graph[curr_node]:
                if adj_node in all_remaining_nodes:
                    all_remaining_nodes.remove(adj_node)
                    bfs_deque.append(adj_node)

        curr_component = get_induced_subgraph(graph, curr_component_nodes)
        components.append(curr_component)

    max_component_len = max([len(component) for component in components])

    for component in components:
        if len(component) == max_component_len:
            return component

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

def get_core():
    # read in graphs
    mouse_graph = read_in_graph('/home/sana/Jurisica/IID/networks/IIDmouse.el')
    rat_graph = read_in_graph('/home/sana/Jurisica/IID/networks/IIDrat.el')

    with open('/extra/wayne1/src/bionets/SANA.github/Jurisica/Migor/IID/IID-mouse-rat-perfect-s3.tsv', 'r') as material_file:
        # read in perfect file
        material_lines = material_file.readlines()[1:]
        relative_weights = list()
        mouse_material_nodes = set()
        rat_material_nodes = set()
        material_mouse_rat_pairs = list()

        for line in material_lines:
            mouse_node, rat_node = re.split('\s', line.strip())
            mouse_material_nodes.add(mouse_node)
            rat_material_nodes.add(rat_node)
            material_mouse_rat_pairs.append((mouse_node, rat_node))

        mouse_material_graph = get_induced_subgraph(mouse_graph, mouse_material_nodes)
        rat_material_graph = get_induced_subgraph(rat_graph, rat_material_nodes)

        # get largest connected component of perfect file
        mouse_material_graph = find_largest_connected_component(mouse_material_graph)
        rat_material_graph = find_largest_connected_component(rat_material_graph)
        assert len(mouse_material_graph) == len(rat_material_graph)
        mouse_material_nodes = set(mouse_material_graph.keys())
        rat_material_nodes = set(rat_material_graph.keys())
        new_material_mouse_rat_pairs = list()

        for mouse_node, rat_node in material_mouse_rat_pairs:
            if mouse_node in mouse_material_nodes:
                assert rat_node in rat_material_nodes
                new_material_mouse_rat_pairs.append((mouse_node, rat_node))

        material_mouse_rat_pairs = new_material_mouse_rat_pairs

        # create population and cumulative distribution
        for mouse_node, rat_node in material_mouse_rat_pairs:
            mouse_degree = len(mouse_material_graph[mouse_node])
            rat_degree = len(rat_material_graph[rat_node])
            assert mouse_degree == rat_degree
            relative_weights.append(mouse_degree)

        # create core graph
        core_mouse_to_rat = dict()
        choices = random.choices(material_mouse_rat_pairs, relative_weights, k = int(CORE_INITIAL_SIZE * 2))

        for mouse_node, rat_node in choices:
            core_mouse_to_rat[mouse_node] = rat_node

            if len(core_mouse_to_rat) == CORE_INITIAL_SIZE:
                break

        mouse_core_nodes = set(core_mouse_to_rat.keys())
        rat_core_nodes = set(core_mouse_to_rat.values())

    mouse_core_graph = get_induced_subgraph(mouse_material_graph, mouse_core_nodes)
    rat_core_graph = get_induced_subgraph(rat_material_graph, rat_core_nodes)

    # assert core graph
    for node, adj in mouse_core_graph.items():
        assert node in mouse_core_nodes
        assert all([adj_node in mouse_core_nodes for adj_node in adj])

    for node, adj in rat_core_graph.items():
        assert node in rat_core_nodes
        assert all([adj_node in rat_core_nodes for adj_node in adj])

    assert len(mouse_core_graph) == len(rat_core_graph) == CORE_INITIAL_SIZE, f'{len(mouse_core_graph)} {len(rat_core_graph)}'

    # find largest connected component
    mouse_core_graph = find_largest_connected_component(mouse_core_graph)
    rat_core_graph = find_largest_connected_component(rat_core_graph)

    # assert again
    for mouse_node in mouse_core_graph:
        corres_rat_node = core_mouse_to_rat[mouse_node]
        assert len(mouse_core_graph[mouse_node]) == len(rat_core_graph[corres_rat_node])

    return mouse_core_graph

def fol_name(i):
    return f'follicle{i}'

def get_fully_grown(core_graph):
    out_graph = copy.deepcopy(core_graph)
    core_size = len(core_graph)
    core_nodes = list(core_graph.keys())

    for i in range(FOLLICLE_COUNT):
        out_graph[fol_name(i)] = list()

    for _ in range(HAIR_COUNT):
        random1 = random.randrange(FOLLICLE_COUNT)
        node1 = fol_name(random1)
        random2 = random.randrange(core_size + FOLLICLE_COUNT)

        if random2 < core_size:
            node2 = core_nodes[random2]
        else:
            node2 = fol_name(random2 - core_size)

        out_graph[node1].append(node2)
        out_graph[node2].append(node1)

    return find_largest_connected_component(out_graph)

def main():
    core_graph = get_core()
    full_graph = get_fully_grown(core_graph)
    print_el(full_graph)

if __name__ == '__main__':
    main()
