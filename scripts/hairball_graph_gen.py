import random
import sys
import re
from collections import defaultdict, deque
import json
import copy
import degree_distr


# SETTINGS
CORE_INITIAL_SIZE = 550
FOLLICLE_COUNT = 4000
FOLLICLE_PRINT_STEP = 300
NUM_NODES = 15000
NUM_EDGES = 300000
left_path = '/home/wangph1/plant/networks/hairball/barabasi_Onl_wcore.el'
right_path = '/home/wangph1/plant/networks/hairball/barabasi_Onr_wcore.el'


# ARGS
if len(sys.argv) == 1:
    CORE_NODES = 1500
    CORE_EDGES = 5000
elif len(sys.argv) == 3:
    CORE_NODES = int(sys.argv[1])
    CORE_EDGES = int(sys.argv[2])
else:
    print('Usage: num args incorrect')


# FUNCTIONS
def debug_print(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

def write_el(graph, fname):
    f = open(fname, 'w')
    el = set()

    for node, adj in graph.items():
        for adj_node in adj:
            min_node = min(node, adj_node)
            max_node = max(node, adj_node)

            if min_node != max_node:
                el.add((min_node, max_node))

    for node1, node2 in el:
        f.write(f'{node1} {node2}\n')

def assert_same_distr(distr1, distr2):
    for key in distr1:
        assert key in distr2

    for key in distr2:
        assert key in distr1

    for key in distr1:
        assert distr1[key] == distr2[key]

def add_distr(distr1, distr2):
    new_distr = dict()

    for key in distr1:
        new_distr[key] = distr1[key]

    for key in distr2:
        if key not in new_distr:
            new_distr[key] = distr2[key]
        else:
            new_distr[key] += distr2[key]

    return new_distr

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

def make_core():
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
            relative_weights.append(1)

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

def core_name(i):
    return f'core{i}'

def grow_erdos_renyi(core_graph):
    out_graph = copy.deepcopy(core_graph)
    core_size = len(core_graph)
    core_nodes = list(core_graph.keys())

    for i in range(FOLLICLE_COUNT):
        out_graph[fol_name(i)] = list()

    for _ in range(HAIR_COUNT):
        random1 = random.randrange(FOLLICLE_COUNT)
        node1 = fol_name(random1)

        while True:
            random2 = random.randrange(core_size + FOLLICLE_COUNT)

            if random2 < core_size:
                node2 = core_nodes[random2]
            else:
                node2 = fol_name(random2 - core_size)

            if node2 != node1:
                break

        out_graph[node1].append(node2)
        out_graph[node2].append(node1)

    return find_largest_connected_component(out_graph)

def gen_random_node_order(size, name_func=fol_name):
    node_order = list()

    for i in range(size):
        node_order.append(name_func(i))

    random.shuffle(node_order)
    return node_order

def gen_connected_graph(size):
    node_order = gen_random_node_order(size)
    out_graph = defaultdict(list)

    for i in range(1, len(node_order)):
        node1 = node_order[i]
        node2 = node_order[random.randrange(i)]
        out_graph[node1].append(node2)
        out_graph[node2].append(node1)

    connected_graph = find_largest_connected_component(out_graph)

    print(f'out_graph is {len(out_graph)} and connected graph is {len(connected_graph)}')
    return out_graph

def gen_barabasi_albert(num_nodes, num_edges, name_func=fol_name):
    node_order = gen_random_node_order(num_nodes, name_func)
    node_pool = [node_order[0]]
    out_graph = defaultdict(list)
    percent_to_print = 0

    for i in range(1, num_edges):
        node1 = node_pool[random.randrange(len(node_pool))]

        if i < len(node_order):
            node2 = node_order[i]
        else:
            node2 = node_pool[random.randrange(len(node_pool))]

        out_graph[node1].append(node2)
        out_graph[node2].append(node1)

        node_pool.append(node1)
        node_pool.append(node2)

        if i * 100 / num_edges > percent_to_print:
            print(f'{percent_to_print}% done')
            percent_to_print += 1

    largest_connected = find_largest_connected_component(out_graph)
    print(f'out_graph is {len(out_graph)} and largest connected is {len(largest_connected)}')
    return largest_connected

def overlay_graph(base_graph, overlay_graph):
    assert len(overlay_graph) <= len(base_graph), 'base graph is smaller than overlay graph'
    base_nodes = list(base_graph.keys())
    random.shuffle(base_nodes)
    replace_nodes = base_nodes[:len(overlay_graph)]
    random.shuffle(replace_nodes)
    remaining_nodes = base_nodes[len(overlay_graph):]

    replace_start_distr = degree_distr.get_sub_degree_distr(base_graph, replace_nodes)
    remaining_start_distr = degree_distr.get_sub_degree_distr(base_graph, remaining_nodes)
    base_start_distr = degree_distr.get_degree_distr(base_graph)
    assert_same_distr(add_distr(replace_start_distr, remaining_start_distr), base_start_distr)

    overlay_nodes = list(overlay_graph.keys())
    random.shuffle(overlay_nodes)
    assert len(overlay_nodes) == len(replace_nodes)
    replace_to_overlay = {replace: overlay for replace, overlay in zip(replace_nodes, overlay_nodes)}
    overlay_to_replace = {overlay: replace for replace, overlay in zip(replace_nodes, overlay_nodes)}
    out_graph = dict()

    # replace all appearances of a replace_node with its overlay_node
    for node, adj in base_graph.items():
        if node in replace_to_overlay:
            out_node = replace_to_overlay[node]
        else:
            out_node = node

        out_graph[out_node] = list()

        for adj_node in adj:
            if adj_node in replace_to_overlay:
                out_adj_node = replace_to_overlay[adj_node]
            else:
                out_adj_node = adj_node

            out_graph[out_node].append(out_adj_node)

    for node in remaining_nodes:
        assert node in out_graph

    for node in replace_nodes:
        assert node not in out_graph

    for node in overlay_nodes:
        assert node in out_graph

    remaining_end_distr = degree_distr.get_sub_degree_distr(out_graph, remaining_nodes)
    overlay_end_distr = degree_distr.get_sub_degree_distr(out_graph, overlay_nodes)
    assert_same_distr(remaining_start_distr, remaining_end_distr)
    assert_same_distr(replace_start_distr, overlay_end_distr)

    # turn overlay distr in out_graph into the actual overlay distr
    for overlay_node in overlay_nodes:
        new_adj = list()

        for adj_node in out_graph[overlay_node]:
            if adj_node not in overlay_nodes:
                new_adj.append(adj_node)

        new_adj.extend(overlay_graph[overlay_node])
        out_graph[overlay_node] = new_adj

    remaining_end_distr = degree_distr.get_sub_degree_distr(out_graph, remaining_nodes)
    assert_same_distr(remaining_start_distr, remaining_end_distr)
    overlay_induced_distr = degree_distr.get_degree_distr(get_induced_subgraph(out_graph, overlay_nodes))
    overlay_og_distr = degree_distr.get_degree_distr(overlay_graph)
    assert_same_distr(overlay_induced_distr, overlay_og_distr)

    return out_graph

def main():
    left_graph = gen_barabasi_albert(15000, 300000)
    write_el(left_graph, '/home/wangph1/plant/networks/hairball/barabasi_300k.el')

    if left_graph != None:
        return

    core_graph = gen_barabasi_albert(CORE_NODES, CORE_EDGES, name_func=core_name)
    left_graph = read_in_graph('/home/wangph1/plant/networks/hairball/barabasi_Onl.el')
    right_graph = read_in_graph('/home/wangph1/plant/networks/hairball/barabasi_Onr.el')
    left_graph = overlay_graph(left_graph, core_graph)
    right_graph = overlay_graph(right_graph, core_graph)

    if left_path != None:
        assert right_path != None
        write_el(left_graph, left_path)
        write_el(right_graph, right_path)
    else:
        assert right_path == None

    print(f'Size of core: {len(core_graph)}')
    print(f'Size of left: {len(left_graph)}')
    print(f'Size of right: {len(right_graph)}')

if __name__ == '__main__':
    main()
