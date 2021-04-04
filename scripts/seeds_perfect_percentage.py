import sys

seed_file = open(sys.argv[1], 'r')
perfect_match_file = open(sys.argv[2] if len(sys.argv) >= 3 else '/extra/wayne1/src/bionets/SANA.github/Jurisica/Migor/IID/IID-mouse-rat-perfect.tsv', 'r')

s1_to_s2 = dict()

for line in perfect_match_file:
    s1_node, s2_node = line.strip().split(' ')
    s1_to_s2[s1_node] = s2_node

matches = 0
total = 0

for line in seed_file:
    seed_id, s1_index_str, s2_index_str = line.strip().split(' ')
    s1_index = s1_index_str.split(',')
    s2_index = s2_index_str.split(',')
    assert(len(s1_index) == len(s2_index))

    for i in range(len(s1_index)):
        if s1_index[i] in s1_to_s2:
            if s1_to_s2[s1_index[i]] == s2_index[i]:
                matches += 1
            else:
                assert False, '{s1_index[i]} is in the CCS but is not matched to {s2_index[i]}'

        total += 1

print(f'{matches} out of {total} nodes were perfect, aka {matches / total * 100}%')
