import re

ORTHO_FILE_PATH = '/home/wayne/src/bionets/SANA/Jurisica/IID/Orthologs.Uniprot.tsv'

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
