#!/bin/python3
import sys

def get_el_from_bv(size, bit_vector):
    el = []

    for left_edge in range(size - 1, -1, -1):
        for bot_edge in range(left_edge - 1, -1, -1):
            if bit_vector % 2 == 1:
                el.append((left_edge, bot_edge))

            bit_vector >>= 1

    return el

def print_el(el):
    print('\n'.join(f'{node1} {node2}' for node1, node2 in el))

if __name__ == '__main__':
    size = int(sys.argv[1])
    bit_vector = int(sys.argv[2])
    print_el(get_el_from_bv(size, bit_vector))
