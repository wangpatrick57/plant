import re

ORTHO_FILE_PATH = '/home/wayne/src/bionets/SANA/Jurisica/IID/Orthologs.Uniprot.tsv'

def get_orthoseeds_list(all_seeds_list, s1_to_s2_orthologs, missing_allowed):
    orthoseeds_list = []

    for graphlet_id, s1_index, s2_index in all_seeds_list:
        missing_nodes = 0

        assert len(s1_index) == len(s2_index), 's1_index length != s2_index length'

        for m in range(len(s1_index)):
            s1_node = s1_index[m]
            s2_node = s2_index[m]

            if s1_node not in s1_to_s2_orthologs or s1_to_s2_orthologs[s1_node] != s2_node:
                missing_nodes += 1

        if missing_nodes <= missing_allowed:
            orthoseeds_list.append((graphlet_id, s1_index, s2_index))

    return orthoseeds_list

def get_orthopairs_list(node_pairs, s1_to_s2_orthologs):
    orthopairs_list = []

    for node1, node2 in node_pairs:
        if node1 in s1_to_s2_orthologs and s1_to_s2_orthologs[node1] == node2:
            orthopairs_list.append((node1, node2))

    return orthopairs_list


def get_s1_to_s2_orthologs(species1, species2):
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
