#!/pkg/python/3.7.4/bin/python3
import re
import math
import sys
from file_helpers import *
from graph_helpers import *

EDGE_LIMIT=400_000

def read_in_temporal_el(graph_path):
    with open(graph_path, 'r') as graph_file:
        tel = []

        for i, line in enumerate(graph_file):
            node1, node2, time = re.split('[\s\t]', line.strip())
            time = int(time)
            tel.append((node1, node2, time))

        return tel

# standard sections are splitting the graph in half by time and then shifting 10% for a total of 10 graphs (ignoring the one with no overlap)
def get_tel_std_sections(tel):
    return get_tel_sections(tel, [0.5] * 4, [0, 0.025, 0.05, 0.1])

def get_tel_sections(tel, length_ratios, offset_ratios):
    assert len(length_ratios) == len(offset_ratios), 'length_ratios must be the same len as offset_ratios' 
    times = [time for node1, node2, time in tel]
    min_time = min(times)
    max_time = max(times)
    total_length = max_time - min_time
    els = []

    for length_ratio, offset_ratio in zip(length_ratios, offset_ratios):
        length = length_ratio * total_length
        offset = offset_ratio * total_length
        start_time = min_time + offset
        end_time = start_time + length
        el = get_el_in_interval(tel, start_time, end_time)
        els.append(el)

    return els

def get_el_in_interval(tel, start_time, end_time):
    el = []

    for node1, node2, time in tel:
        if start_time <= time < end_time:
            el.append((node1, node2))

    return el

# start time is inclusive, end time is exclusive
def read_in_xel_in_interval(graph_path, start_time, end_time, is_tel=True):
    with open(graph_path, 'r') as graph_file:
        xel = []

        for line in graph_file:
            node1, node2, time = re.split('[\s\t]', line.strip())
            time = int(time)

            if time >= end_time:
                break

            if time >= start_time:
                edge = [source, target]

                if is_tel:
                    edge.append(str(int(float(time))))

                edge = tuple(edge)
                xel.append(edge)

        return xel

# a no_t_tel is basically an ordered set (ordered and unique)
def get_no_t_tel(tel):
    no_t_tel = []
    added_edges = set()

    for node1, node2, time in tel:
        if node1 == node2:
            continue

        edge = get_canon_edge(node1, node2)

        if edge not in added_edges:
            added_edges.add(edge)
            no_t_tel.append(edge)

    print('len(tel):', len(tel))
    print('len(no_t_tel):', len(no_t_tel))
    print('len(added_edges):', len(added_edges))
    return no_t_tel

# TODO
def get_el_from_nttel_with_limits(no_t_tel, num_skipped_edges, node_limit=20_000, edge_limit=EDGE_LIMIT, density_limit=20, total_edge_ratio_limit=10/11):
    from graph_helpers import nodes_of_el

    tel_max_edges = len(no_t_tel) * total_edge_ratio_limit
    max_edges = min(edge_limit, tel_max_edges)
    num_edges = 0
    nodes = set()
    total_nodes = len(nodes_of_el(no_t_tel))
    el = []
    nttel_slice = no_t_tel[num_skipped_edges:]

    for node1, node2 in nttel_slice:
        if num_edges >= max_edges:
            break

        num_nodes = len(nodes)
        
        if num_nodes >= node_limit:
            break

        if num_nodes >= total_nodes / 100:
            if num_edges / num_nodes >= density_limit:
                break

        edge = get_canon_edge(node1, node2)

        if edge != None:
            el.append(edge)
            nodes.add(node1)
            nodes.add(node2)
        else:
            assert node1 in nodes and node2 in nodes

        num_edges += 1

    return el

def get_std_percents():
    return [0, 1, 5, 10]

def get_gtag_from_tgtag(tgtag, percent):
    return f'{tgtag}_s{percent}'

def gen_std_tgtag_els(tgtag):
    from graph_helpers import el_to_str
    from file_helpers import write_to_file

    ntpath = get_nttgraph_path(tgtag)
    nttel = read_in_nttel(ntpath)
    num_edges = len(nttel)

    for percent in get_std_percents():
        num_skipped_edges = num_edges * percent // 100
        el = get_el_from_nttel_with_limits(nttel, num_skipped_edges)
        new_gtag = get_gtag_from_tgtag(tgtag, percent)
        new_path = get_graph_path(new_gtag)
        el_str = el_to_str(el)
        write_to_file(el_str, new_path)

def map_density_over_time(tel, granularity=100):
    times = [int(row[2]) for row in tel]
    start_time = min(times)
    end_time = max(times) + 1
    tbins = [0] * granularity

    for time in times:
        tbin_num = math.floor((time - start_time) * granularity / (end_time - start_time))
        tbins[tbin_num] += 1

    for i, lines_in_this_range in enumerate(tbins):
        this_start_time = start_time + (end_time - start_time) * i / granularity
        print(this_start_time, lines_in_this_range)

def get_tgraph_path(tgtag):
    from graph_helpers import get_base_graph_path
    return get_base_graph_path(f'snap/{tgtag}', ext='tel')

def get_nttgraph_path(tgtag):
    from graph_helpers import get_base_graph_path
    return get_base_graph_path(f'snap/{tgtag}', ext='nttel')

# not using graph_helpers.el_to_str because that's not defined to maintain order
def nttel_to_str(nttel):
    return '\n'.join(f'{node1}\t{node2}' for node1, node2 in nttel)

# not using graph_helpers.read_in_el because that's not defined to maintain order
def read_in_nttel(path):
    with open(path, 'r') as f:
        nttel = []

        for line in f:
            node1, node2 = line.strip().split('\t')
            canon_edge = get_canon_edge(node1, node2)

            if canon_edge != None:
                nttel.append(canon_edge)

        return nttel

def get_canon_edge(node1, node2):
    assert node1 != node2 # putting this assert in this function is just a convenient way to make sure it's usually called
        
    return (min(node1, node2), max(node1, node2))

# canonizes edges and ignores self edges
def gen_nttel_file(tgtag, max_unique_edges=EDGE_LIMIT):
    from file_helpers import write_to_file

    tel_path = get_tgraph_path(tgtag)

    with open(tel_path) as tel_f:
        unique_edges = set()
        nttel = []

        for line in tel_f:
            if len(unique_edges) >= max_unique_edges:
                break

            node1, node2, time = line.strip().split()

            if node1 == node2:
                continue

            edge = get_canon_edge(node1, node2)

            if edge not in unique_edges:
                unique_edges.add(edge)
                nttel.append(edge)

        nttel_path = get_nttgraph_path(tgtag)
        write_to_file(nttel_to_str(nttel), nttel_path)
        return

    print(f'failed to write nttel for {tgtag}')

if __name__ == '__main__':
    from graph_helpers import get_paper_tprl_snap

    for tgtag in get_paper_tprl_snap():
        gen_std_tgtag_els(tgtag)
