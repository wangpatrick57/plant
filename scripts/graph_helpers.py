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
