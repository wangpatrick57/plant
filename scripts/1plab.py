#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

species = ["cat","cow","dog","guineapig","horse","human","mouse","pig","rabbit","rat","sheep"]

for first_specie in range(0, len(species) - 1):
    for second_specie in range(first_specie + 1, len(species)):
        with open("mapping.out", 'w') as f:
            f.seek(0) # Deleting existing info for the next run
            f.truncate() # Deleting existing info for the next run
            first_adj_set = cache_read_in_adj_set(species[first_specie])
            second_adj_set = cache_read_in_adj_set(species[second_specie])
            first_top_nodes = get_top_nodes(first_adj_set, 10)
            second_top_nodes = get_top_nodes(second_adj_set, 10)
            for i in range(10):
                f.write(first_top_nodes[i][0] + " " + second_top_nodes[i][0])
                f.write('\n')
            f.close()

            first_result = list_of_nodes_from_species("../networks/iid/" + species[first_specie] + ".el")
            second_result = list_of_nodes_from_species("../networks/iid/" + species[second_specie] + ".el")

            mapping = filtering_lists("mapping.out")
            mapping1 = set(mapping)
            lines1 = set()
            lines2 = set()
            for i in mapping:
                lines1.add(i[0])
                lines2.add(i[1])

            edges1 = add_valid_edges(first_result, lines1) # left valid edges
            edges2 = add_valid_edges(second_result, lines2) # right valid edges
            consistentEdges1 = num_consistent_edges(edges1, edges2, mapping1)

            totalConsistency = float(consistentEdges1) / max(edges1[1], edges2[1])

            print(species[first_specie] + " " + species[second_specie] + " " + str(totalConsistency))
            