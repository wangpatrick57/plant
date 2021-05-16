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
    mouse_og_fname = '/home/sana/Jurisica/IID/networks/IIDmouse.el'
    rat_og_fname = '/home/sana/Jurisica/IID/networks/IIDrat.el'
    all_fnames = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    rat_low_fnames, rat_high_fnames = get_low_and_high(all_fnames, 'rat', {4}, NUM_TRIALS)
    rat_og_edge_set = get_edge_set(rat_og_fname)
    low_removed_edge_sets = list()
    high_removed_edge_sets = list()
    low_added_edge_sets = list()
    high_added_edge_sets = list()

    for rat_low_fname in rat_low_fnames:
        this_edge_set = get_edge_set(data_dir + rat_low_fname)
        this_removed_edge_set = rat_og_edge_set - this_edge_set
        this_added_edge_set = this_edge_set - rat_og_edge_set
        low_removed_edge_sets.append(this_removed_edge_set)
        low_added_edge_sets.append(this_added_edge_set)
        print(rat_low_fname)
        print(len(this_removed_edge_set))
        print(len(this_added_edge_set))
        print(len(this_removed_edge_set & this_added_edge_set))

    print('\n'.join(['\t'.join(edge_str.split(',')) for edge_str in low_added_edge_sets[0]]), file=sys.stderr)
    return

    for rat_high_fname in rat_high_fnames:
        this_edge_set = get_edge_set(data_dir + rat_high_fname)
        this_removed_edge_set = rat_og_edge_set - this_edge_set
        this_added_edge_set = this_edge_set - rat_og_edge_set
        high_removed_edge_sets.append(this_removed_edge_set)
        high_added_edge_sets.append(this_added_edge_set)
        print(rat_high_fname)
        print(len(this_removed_edge_set))
        print(len(this_added_edge_set))
        print(len(this_removed_edge_set & this_added_edge_set))

if __name__ == '__main__':
    main()
