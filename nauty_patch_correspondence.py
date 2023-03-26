import sys

ids_file = open(sys.argv[1], 'r')
patchids_file = open(sys.argv[2], 'r')
nautyid_to_labels = dict()
nautyid_to_multiplicity = dict()

for patchid, line in zip(patchids_file, ids_file):
    line_split = line.strip().split()
    patchid = patchid.strip()
    nautyid = line_split[0]
    multiplicity = int(line_split[1])

    nautyid_to_multiplicity[nautyid] = multiplicity

    labels_str = ' '.join(line_split[2:])

    if nautyid not in nautyid_to_labels:
        nautyid_to_labels[nautyid] = dict()

    if labels_str not in nautyid_to_labels[nautyid]:
        nautyid_to_labels[nautyid][labels_str] = set()

    nautyid_to_labels[nautyid][labels_str].add(patchid)

for nautyid, labels_dict in nautyid_to_labels.items():
    if len(labels_dict) == 1:
        continue

    if nautyid_to_multiplicity[nautyid] == 0:
        continue

    for labels_str, patchid_set in labels_dict.items():
        print(f'nautyid {nautyid} corresponds to labels_str {labels_str}, which corresponds to the following patchids: {patchid_set}')

    print()
