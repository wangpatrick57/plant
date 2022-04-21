#!/bin/python3
def get_all_species():
    return ['cat', 'cow', 'guinea_pig', 'horse', 'human', 'mouse', 'pig', 'rabbit', 'rat']
    # return ['guinea_pig', 'horse', 'human', 'mouse', 'pig', 'rabbit', 'rat']
    # return ['guinea_pig', 'horse', 'human']
    # return ['mouse', 'pig', 'rabbit', 'rat']

def get_all_species_pairs():
    all_species_pairs = set()

    for species1 in get_all_species():
        for species2 in get_all_species():
            if species1 != species2:
                all_species_pairs.add(tuple(sorted((species1, species2))))

    return all_species_pairs

if __name__ == '__main__':
    print(get_all_species_pairs())
    print(len(get_all_species_pairs()))
