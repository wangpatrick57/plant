#!/bin/python3
import sys
import bv2el
import re

def get_bv_from_ord(ord, ord_content):
    return int(re.split('[\s]+', ord_content[ord + 1])[0])

def get_inced_el(el, n):
    inced_el = []

    for node1, node2 in el:
        inced_el.append((node1 + n, node2 + n))

    return inced_el

def get_combined_el(el1, el2):
    combined_el = []

    for el in [el1, el2]:
        for node1, node2 in el:
            combined_el.append((node1, node2))

    return combined_el

def get_replaced_el(el, replace_dict):
    replaced_el = []

    for node1, node2 in el:
        if node1 in replace_dict:
            new_node1 = replace_dict[node1]
        else:
            new_node1 = node1

        if node2 in replace_dict:
            new_node2 = replace_dict[node2]
        else:
            new_node2 = node2

        replaced_el.append((new_node1, new_node2))

    return replaced_el

def get_el_from_patchid(size, patchid):
    # split
    ord1, ord2, match, extra = patchid.split(';')

    # get initial two graphettes
    ord1 = int(ord1)
    ord2 = int(ord2)
    ord_file = open(f'/home/wangph1/oldBLANT/BLANT/canon_maps/canon_list{size}.txt')
    ord_content = ord_file.readlines()
    bv1 = get_bv_from_ord(ord1, ord_content)
    bv2 = get_bv_from_ord(ord2, ord_content)
    el1 = bv2el.get_el_from_bv(size, bv1)
    el2 = bv2el.get_el_from_bv(size, bv2)
    el2 = get_inced_el(el2, 10)
    final_el = get_combined_el(el1, el2)

    # match
    replace_dict = dict()

    for pair in match.split(','):
        node1, node2 = pair.split(':')
        node1 = int(node1)
        node2 = int(node2)
        replace_dict[node2 + 10] = node1

    final_el = get_replaced_el(final_el, replace_dict)
    
    # extra
    if extra != '':
        extra_el = []

        for list_row in extra.split('-'):
            base_node, adj_nodes = list_row.split(':')
            base_node = int(base_node)

            for adj_node in adj_nodes.split(','):
                adj_node = int(adj_node)
                extra_el.append((base_node, adj_node + 10))

        final_el = get_combined_el(final_el, extra_el)
        bv2el.print_el(final_el)

    # convert to canonical order
    left_matching = set()
    right_matching = set()

    for pair in match.split(','):
        node1, node2 = pair.split(':')
        node1 = int(node1)
        node2 = int(node2)
        left_matching.add(node1)
        right_matching.add(node2 + 10)

    canonical_order = []

    for left_node in range(0, size):
        if left_node not in left_matching:
            canonical_order.append(left_node)

    for left_node in range(0, size):
        if left_node in left_matching:
            canonical_order.append(left_node)

    for right_node in range(10, size + 10):
        if right_node not in right_matching:
            canonical_order.append(right_node)

    replace_dict = dict()

    for i, node in enumerate(canonical_order):
        replace_dict[node] = i

    print(canonical_order)
    print(replace_dict)
    final_el = get_replaced_el(final_el, replace_dict)

    return final_el

if __name__ == '__main__':
    size = int(sys.argv[1])
    patchid = sys.argv[2]
    bv2el.print_el(get_el_from_patchid(size, patchid))
