#!/pkg/python/3.7.4/bin/python3
import random
import re
import sys

NOISE_LETTERS = ['a', 'b']

def get_noisy_el(el, noise_num):
    noisy_el = []
    noise_dec = noise_num / 100

    for edge in el:
        if random.random() >= noise_dec:
            noisy_el.append(edge)

    return noisy_el

def get_noisy_gtag(gtag, noise_num, version_num, letter):
    assert letter in NOISE_LETTERS
    return f'{gtag}_{noise_num}v{version_num}{letter}'

def is_noisy_gtag(gtag):
    noisy_gtag_re = '_[0-9]+v[0-9]+[ab]$'
    return re.search(noisy_gtag_re, gtag) != None

def get_noisy_graph_path(gtag):
    from graph_helpers import get_base_graph_path

    return get_base_graph_path(f'noise/{gtag}')

def gen_noisy_el_pair(gtag, noise_num, version_num):
    from graph_helpers import read_in_el, get_graph_path, el_to_str
    from file_helpers import write_to_file, file_exists

    el = read_in_el(get_graph_path(gtag))

    for letter in NOISE_LETTERS:
        noisy_gtag = get_noisy_gtag(gtag, noise_num, version_num, letter)
        path = get_graph_path(noisy_gtag)

        if file_exists(path):
            print(f'{path} already exists')
        else:
            noisy_el = get_noisy_el(el, noise_num)
            write_to_file(el_to_str(noisy_el), path)

if __name__ == '__main__':
    gen_noisy_el_pair(gtag)
