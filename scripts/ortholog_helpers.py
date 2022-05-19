import re
from graph_helpers import *

ORTHO_FILE_PATH = '/home/wayne/src/bionets/SANA/Jurisica/IID/Orthologs.Uniprot.tsv'

class SelfOrthos(dict):
    def __setitem__(self, key):
        raise AssertionError

    def __getitem__(self, key):
        return key


def get_avg_node_correctness(all_seeds, g1_to_g2_orthologs):
    nc_sum = 0

    for gid, align1, align2 in all_seeds:
        num_correct_nodes = 0
        assert len(align1) == len(align2)

        for node1, node2 in zip(align1, align2):
            if is_ortholog(node1, node2, g1_to_g2_orthologs):
                num_correct_nodes += 1

        nc_sum += num_correct_nodes / len(align1)

    return nc_sum / len(all_seeds)

def get_ortho_coverage(all_seeds, g1_to_g2_orthologs):
    orthonodes1 = set()
    orthonodes2 = set()
    g1_orthonodes = set(g1_to_g2_orthologs.keys())
    g2_orthonodes = set(g1_to_g2_orthologs.values())

    for gid, align1, align2 in all_seeds:
        for node in align1:
            if node in g1_orthonodes:
                orthonodes1.add(node)

        for node in align2:
            if node in g2_orthonodes:
                orthonodes2.add(node)

    print(len(orthonodes1), len(orthonodes2))
    return min(len(orthonodes1), len(orthonodes2))

def get_orthoseeds_list(all_seeds_list, s1_to_s2_orthologs, missing_allowed=0):
    orthoseeds_list = []

    for graphlet_id, s1_index, s2_index in all_seeds_list:
        missing_nodes = 0

        assert len(s1_index) == len(s2_index), 's1_index length != s2_index length'

        for m in range(len(s1_index)):
            s1_node = s1_index[m]
            s2_node = s2_index[m]

            if not is_ortholog(node1, node2, s1_to_s2_orthologs):
                missing_nodes += 1

        if missing_nodes <= missing_allowed:
            orthoseeds_list.append((graphlet_id, s1_index, s2_index))

    return orthoseeds_list

def get_orthopairs_list(node_pairs, s1_to_s2_orthologs):
    orthopairs_list = []

    for node1, node2 in node_pairs:
        if is_ortholog(node1, node2, s1_to_s2_orthologs):
            orthopairs_list.append((node1, node2))

    return orthopairs_list

def is_ortholog(node1, node2, s1_to_s2_orthologs):
    if type(s1_to_s2_orthologs) is SelfOrthos:
        return node1 == node2
    
    return node1 in s1_to_s2_orthologs and s1_to_s2_orthologs[node1] == node2

def get_g1_to_g2_orthologs(gtag1, gtag2):
    g1_is_species = is_species(gtag1)
    g2_is_species = is_species(gtag2)

    if g1_is_species != g2_is_species:
        raise AssertionError

    if g1_is_species:
        return get_s1_to_s2_orthologs(gtag1, gtag2)
    else:
        print('test')
        return SelfOrthos()

def get_s1_to_s2_orthologs(species1, species2):
    if 'syeast' in species1 or 'syeast' in species2:
        assert 'syeast' in species1 and 'syeast' in species2, 'syeast must be in both or neither'
        s1_to_s2 = dict()
        syeast0_path = get_graph_path('syeast0')
        nodes = read_in_nodes(syeast0_path)

        for node in nodes:
            s1_to_s2[node] = node

        return s1_to_s2

    with open(ORTHO_FILE_PATH, 'r') as ortho_file:
        species_to_index = dict()
        species_line = ortho_file.readline().strip()
        species_order = re.split('[\s\t]+', species_line)

        for i, species in enumerate(species_order):
            species_to_index[species] = i

        s1_to_s2 = dict()
        s1_pos = species_to_index[species1]
        s2_pos = species_to_index[species2]

        for line in ortho_file:
            line_split = line.strip().split()

            if line_split[s1_pos] == species1: # first line
                assert line_split[s2_pos] == species2
            else: # other lines
                s1_node = line_split[s1_pos]
                s2_node = line_split[s2_pos]

                if s1_node != '0' and s2_node != '0':
                    s1_to_s2[s1_node] = s2_node

        return s1_to_s2

if __name__ == '__main__':
    s1_to_s2_orthologs = get_s1_to_s2_orthologs('mouse', 'rat')
