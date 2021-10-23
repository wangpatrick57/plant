import os
import re
import sys

def get_filtered_fnames(fnames, species, nums):
    return [f for f in fnames if  # loop through all filenames
            any(num_str in f for num_str in  # keep the ones that have ANY of the nums..
                [f'_{num}.el' for num in nums])  # ..by converting them to strs that include the file format
            and species in f]  # and of those, only keep those of the desired species

def get_low_and_high(fnames, species, low_nums, max_num):
    high_nums = set(range(1, max_num + 1)) - low_nums
    print('low', low_nums, file=sys.stderr)
    print('high', high_nums, file=sys.stderr)
    return get_filtered_fnames(fnames, species, low_nums), get_filtered_fnames(fnames, species, high_nums)

def get_edge_set(fname):
    f = open(fname, 'r')
    edge_set = set()

    for line in f:
        node1, node2 = re.split('\s', line.strip())
        
        if node1 > node2:
            node1, node2 = node2, node1

        edge_set.add(','.join((node1, node2)))

    f.close()
    return edge_set

def main():
    NUM_TRIALS = 5
    data_dir = '/home/wangph1/plant/networks/perturb/'
    species = sys.argv[1]
    og_fname = f'/home/sana/Jurisica/IID/networks/IID{species}.el'
    all_fnames = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    low_fnames, high_fnames = get_low_and_high(all_fnames, species, {int(sys.argv[2])}, NUM_TRIALS)
    og_edge_set = get_edge_set(og_fname)
    low_removed_edge_sets = list()
    high_removed_edge_sets = list()
    low_added_edge_sets = list()
    high_added_edge_sets = list()

    for low_fname in low_fnames:
        this_edge_set = get_edge_set(data_dir + low_fname)
        this_removed_edge_set = og_edge_set - this_edge_set
        this_added_edge_set = this_edge_set - og_edge_set
        low_removed_edge_sets.append(this_removed_edge_set)
        low_added_edge_sets.append(this_added_edge_set)
        print(low_fname, file=sys.stderr)
        print(len(this_removed_edge_set), file=sys.stderr)
        print(len(this_added_edge_set), file=sys.stderr)
        print(len(this_removed_edge_set & this_added_edge_set), file=sys.stderr)

    print('\n'.join(['\t'.join(edge_str.split(',')) for edge_str in low_removed_edge_sets[-1]]))
    return

    for high_fname in high_fnames:
        this_edge_set = get_edge_set(data_dir + high_fname)
        this_removed_edge_set = og_edge_set - this_edge_set
        this_added_edge_set = this_edge_set - og_edge_set
        high_removed_edge_sets.append(this_removed_edge_set)
        high_added_edge_sets.append(this_added_edge_set)
        print(high_fname)
        print(len(this_removed_edge_set))
        print(len(this_added_edge_set))
        print(len(this_removed_edge_set & this_added_edge_set))

if __name__ == '__main__':
    main()
