#!/bin/python3
def assert_with_prints(value, target, value_title):
    assert value == target, f'{value_title} is not {target}'
    print(f'success, {value_title} = {target}')

def species_to_full_name(species):
    if 'syeast' in species:
        return species
    else:
        return f'IID{species}'

def calc_f1(orth, found, n):
    tp = orth
    fp = found - orth
    fn = n - orth
    return tp / (tp + 0.5 * (fp + fn))

def print_dict(d):
    print('\n'.join([f'{k}\t{v}' for k, v in d.items()]))

if __name__ == '__main__':
    assert_with_prints(5, 5, 'foo')
