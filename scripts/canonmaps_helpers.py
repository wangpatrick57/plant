#!/bin/python3
# helpers for the canon_maps/ directory
from collections import namedtuple
from file_helpers import *

CanonListLine = namedtuple('CanonListLine', ['connected', 'num_edges', 'edges'])

def get_canon_list_path(k):
    return get_blant_path(f'canon_maps/canon_list{k}.txt')

def get_orbit_map_path(k):
    return get_blant_path(f'canon_maps/orbit_map{k}.txt')

def read_in_canon_list(k):
    canon_list_path = get_canon_list_path(k)
    canon_list = dict()

    with open(canon_list_path, 'r') as f:
        num = None
    
        for line in f:
            line = line.strip()
            
            if num == None:
                num = int(line)
            else:
                splitted = line.split('\t')
                bv = int(splitted[0])
                connected = bool(int(splitted[1].split(' ')[0]))
                num_edges = int(splitted[1].split(' ')[1])
                
                if len(splitted) <= 2:
                    edges = []
                else:
                    edges = [tuple(map(int, edge_str.split(','))) for edge_str in splitted[2].split(' ')]
                    
                canon_list[bv] = CanonListLine(connected, num_edges, edges)

    assert len(canon_list) == num
    return canon_list

def get_bvs_in_order(orbit_list):
    return sorted(orbit_list.keys())

def read_in_orbit_map(k, bvs_in_order):
    orbit_map_path = get_orbit_map_path(k)
    orbit_map = dict()

    with open(orbit_map_path, 'r') as f:
        num = None
        bv_ordinal = 0
    
        for line in f:
            line = line.strip()
            
            if num == None:
                num = int(line)
            else:
                bv = bvs_in_order[bv_ordinal]
                orbits = tuple(map(int, line.split(' ')))
                orbit_map[bv] = orbits
                bv_ordinal += 1

    assert len(orbit_map) == len(bvs_in_order)
    assert orbit_map[bvs_in_order[-1]][-1] == num - 1
    return orbit_map

def read_in_canon_list_and_orbit_map(k):
    canon_list = read_in_canon_list(k)
    bvs_in_order = get_bvs_in_order(canon_list)
    orbit_map = read_in_orbit_map(k, bvs_in_order)
    return canon_list, orbit_map

# This graphlet is actually not generated using the bitvector itself (which bv2el.py does). Instead, it uses the bitvector as an ID into the canon_list and orbit_map to generate the graphlet. It also has the orbit nodes correctly labeled as in networks/graphlets/
def get_bv_el_with_blantitl_orbit_nodes(bv, canon_list, orbit_map):
    el = []
    edges = canon_list[bv].edges
    orbits = orbit_map[bv]
    orbit_ascii_map = {orbit: 97 for orbit in set(orbits)}
    orbit_nodes = []

    for orbit in orbits:
        orbit_nodes.append(f'{orbit}{chr(orbit_ascii_map[orbit])}')
        orbit_ascii_map[orbit] += 1

    for i, j in edges:
        el.append((orbit_nodes[i], orbit_nodes[j]))

    return el
