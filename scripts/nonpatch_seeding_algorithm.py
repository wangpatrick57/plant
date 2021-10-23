from collections import defaultdict
import sys
import re

# settings
MISSING_ALLOWED = 1

# input
k = int(sys.argv[1])
species1 = sys.argv[2]
species2 = sys.argv[3]
s1_index_file = open(sys.argv[4])
s2_index_file = open(sys.argv[5])
speedup = int(sys.argv[6]) if len(sys.argv) > 6 else 1
which_to_print = sys.argv[7] if len(sys.argv) > 7 else "ORTHO"

# ortho stuff
ortho_file = open('/home/wayne/src/bionets/SANA/Jurisica/IID/Orthologs.Uniprot.tsv', 'r')
SPECIES_TO_INDEX = dict()
species_line = ortho_file.readline().strip()
species_order = re.split('[\s\t]+', species_line)

for i, species in enumerate(species_order):
    SPECIES_TO_INDEX[species] = i

s1_to_s2 = dict()
s1_pos = SPECIES_TO_INDEX[species1]
s2_pos = SPECIES_TO_INDEX[species2]

for line in ortho_file:
    line_split = line.strip().split()

    if line_split[s1_pos] == species1: # first line
        assert line_split[s2_pos] == species2
    else: # other lines
        s1_node = line_split[s1_pos]
        s2_node = line_split[s2_pos]

        if s1_node != '0' and s2_node != '0':
            s1_to_s2[s1_node] = s2_node

print(len(s1_to_s2.values()), len(set(s1_to_s2.values())), file=sys.stderr)

# read in species1 index file
s1_indexes = defaultdict(list)

for i, line in enumerate(s1_index_file):
    line_split = line.strip().split()
    assert len(line_split) == k + 1, f'{i}: {line.strip()}'
    graphlet_id = int(line_split[0])
    index = line_split[1:]
    s1_indexes[graphlet_id].append(index)

# read in species2 index file
s2_indexes = defaultdict(list)

for i, line in enumerate(s2_index_file):
    line_split = line.strip().split()
    assert len(line_split) == k + 1, f'{i}: {line.strip()}'
    graphlet_id = int(line_split[0])
    index = line_split[1:]
    s2_indexes[graphlet_id].append(index)

# calculate total graphlet pairs
total_graphlet_pairs = 0

for graphlet_id, s1_graphlet_indexes in s1_indexes.items():
    if graphlet_id in s2_indexes:
        total_graphlet_pairs += len(s1_graphlet_indexes) * len(s2_indexes[graphlet_id])

total_pairs_to_process = int(total_graphlet_pairs / (speedup ** 2))

print(f'total_graphlet_pairs: {total_graphlet_pairs}', file=sys.stderr)
print(f'total_pairs_to_process: {total_pairs_to_process}', file=sys.stderr)

# calc orthoseeds
orthoseeds_list = []
all_seeds_list = []
percent_printed = 0

for graphlet_id, s1_graphlet_indexes in s1_indexes.items():
    if len(s1_graphlet_indexes) > 3:
        continue

    if graphlet_id in s2_indexes:
        if len(s2_indexes[graphlet_id]) > 3:
            continue

        for i in range(0, len(s1_graphlet_indexes), speedup):
            s1_index = s1_graphlet_indexes[i]

            for j in range(0, len(s2_indexes[graphlet_id]), speedup):
                s2_index = s2_indexes[graphlet_id][j]
                missing_nodes = 0
                
                for m in range(k):
                    s1_node = s1_index[m]
                    s2_node = s2_index[m]

                    if s1_node not in s1_to_s2 or s1_to_s2[s1_node] != s2_node:
                        missing_nodes += 1

                        if missing_nodes > MISSING_ALLOWED:
                            break
                        
                if missing_nodes <= MISSING_ALLOWED:
                    orthoseeds_list.append((graphlet_id, s1_index, s2_index))

                all_seeds_list.append((graphlet_id, s1_index, s2_index))

                # print
                pairs_processed = len(all_seeds_list)
                
                if pairs_processed / total_pairs_to_process * 100 > percent_printed:
                    print(f'{percent_printed}% done', file=sys.stderr)
                    percent_printed += 1

# spit out value and percent
pairs_processed = len(all_seeds_list)
list_to_print = orthoseeds_list if which_to_print == "ORTHO" else all_seeds_list
list_to_print_str = '\n'.join(f'{str(graphlet_id) + " " + ",".join(s1_seed) + " " + ",".join(s2_seed)}' for graphlet_id, s1_seed, s2_seed in list_to_print)
print(list_to_print_str)
print(f'there are {len(orthoseeds_list)} {k - MISSING_ALLOWED}|{k} orthoseeds out of {pairs_processed} processed graphlet pairs, representing {len(orthoseeds_list) * 100 / pairs_processed}%', file=sys.stderr)
