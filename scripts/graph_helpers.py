import re

def get_graph_fname_from_species(species):
    return f'/home/sana/Jurisica/IID/networks/IID{species}.el'

def read_adj_set(graph_file):
    adj_set = dict()

    for edge_str in graph_file:
        node1, node2 = re.split('[\s\t]', edge_str.strip())

        if node1 not in adj_set:
            adj_set[node1] = set()

        if node2 not in adj_set:
            adj_set[node2] = set()

        adj_set[node1].add(node2)
        adj_set[node2].add(node1)

    return adj_set

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

def get_si_to_sj(speciesi, speciesj, ortho_file):
    species_to_index = dict()
    species_line = ortho_file.readline().strip()
    species_order = re.split('[\s\t]+', species_line)

    for i, species in enumerate(species_order):
        species_to_index[species] = i

    si_to_sj = dict()
    si_pos = species_to_index[speciesi]
    sj_pos = species_to_index[speciesj]

    for line in ortho_file:
        line_split = line.strip().split()

        if line_split[si_pos] == speciesi: # first line
            assert line_split[sj_pos] == speciesj
        else: # other lines
            si_node = line_split[si_pos]
            sj_node = line_split[sj_pos]

            if si_node != '0' and sj_node != '0':
                si_to_sj[si_node] = sj_node

    return si_to_sj

def get_num_missing(s1_index, s2_index, s1_to_s2):
    missing_nodes = 0

    assert len(s1_index) == len(s2_index)

    for m in range(len(s1_index)):
        s1_node = s1_index[m]
        s2_node = s2_index[m]

        if s1_node not in s1_to_s2 or s1_to_s2[s1_node] != s2_node:
            missing_nodes += 1

    return missing_nodes
