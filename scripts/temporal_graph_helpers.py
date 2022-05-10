#!/pkg/python/3.7.4/bin/python3
import re
import math
import sys
from file_helpers import *
from graph_helpers import *

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
    times = [time for node1, node2, time in tel]
    min_time = min(times)
    max_time = max(times)
    length = (max_time - min_time) / 2
    els = []

    for i in range(10):
        start_time = min_time + i * length / 10
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
def read_in_el_in_interval(graph_path, start_time, end_time):
    with open(graph_path, 'r') as graph_file:
        el = []

        for line in graph_file:
            node1, node2, time = re.split('[\s\t]', line.strip())
            time = int(time)

            if time >= end_time:
                break

            if time >= start_time:
                el.append((node1, node2))

        return el

def read_in_el_until_edge_limit(graph_path, start_time, edge_limit):
    nodes, edges, interval = read_in_nodges_until_nodge_limit(graph_path, start_time, edge_limit=edge_limit)
    el = list(edges)
    return el

def read_in_nodges_until_nodge_limit(graph_path, start_time, node_limit=None, edge_limit=None):
    if node_limit == None and edge_limit == None:
        return

    if node_limit != None and edge_limit != None:
        return

    with open(graph_path, 'r') as graph_file:
        edges = set()
        nodes = set()

        for line in graph_file:
            node1, node2, time = re.split('[\s\t]', line.strip())
            time = int(time)

            if edge_limit != None and len(edges) >= edge_limit:
                end_time = time
                break

            if node_limit != None and len(nodes) >= node_limit:
                end_time = time
                break

            if time >= start_time:
                edges.add((node1, node2))
                nodes.add(node1)
                nodes.add(node2)

    return (nodes, edges, end_time - start_time)

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

def get_edge_limit_node_edge_ratios(graph_path, start_time, interval, count, edge_limit):
    time = start_time

    for _ in range(count):
        nodes, edges, interval = read_in_nodges_until_nodge_limit(graph_path, time, edge_limit=edge_limit)
        print(f'{time}\t{len(nodes)}\t{interval}')
        time += interval

def get_node_limit_node_edge_ratios(graph_path, start_time, interval, count, node_limit):
    time = start_time

    for _ in range(count):
        nodes, edges, interval = read_in_nodges_until_nodge_limit(graph_path, time, node_limit=node_limit)
        print(f'{time}\t{len(edges)}\t{interval}')
        time += interval

if __name__ == '__main__':
    base = sys.argv[1]
    tel = read_in_temporal_el(f'../networks/snap/{base}.tel')
    els = get_tel_std_sections(tel)

    for i, el in enumerate(els):
        write_el_to_file(el, f'../networks/snap/{base}{i}.el')
        graph_stats(el, f'{base}{i}')
