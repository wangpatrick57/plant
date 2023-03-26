#!/bin/python3
from index_helpers import *
from graph_helpers import *

def validate_index_file(index_path, k):
    try:
        with open(index_path, 'r') as index_file:
            for entry_str in index_file:
                if len(entry_str.strip().split(' ')) != k + 1:
                    return False
        
            return True
    except FileNotFoundError:
        print(f'file {index_path} not found')
        return False
    except:
        raise

def validate_range(k, species_list, percent_list=[0], orbit_list=[0]):
    for species in species_list:
        for percent in percent_list:
            for orbit in orbit_list:
                is_valid = validate_index_file(get_index_path(species, percent=percent, orbit=orbit), k)

                if not is_valid:
                    print(f'{species} p{percent} o{orbit} is not valid')

def validate_paper_all(algo='stairs'):
    from graph_helpers import get_paper_all_gtags

    for gtag in get_paper_all_gtags():
        path = get_index_path(gtag, algo=algo)
        valid = validate_index_file(path, 8)

        if not valid:
            print(f'{gtag} is invalid')

if __name__ == '__main__':
    validate_paper_all(algo='stairs')
