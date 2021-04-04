import sys
import re


# get input
k = int(sys.argv[1])
s1_graph_file = open(sys.argv[2], 'r')
s2_graph_file = open(sys.argv[3], 'r')
seeds_file = open(sys.argv[4], 'r')
s1_indexes_file = open(sys.argv[5], 'r')
s2_indexes_file = open(sys.argv[6], 'r')


# create adjacency lists
def fill_adj_list(adj_list, graph_file):
    for line in graph_file:
        node1, node2 = re.split('[\s\t]', line.strip())

        if node1 not in adj_list:
            adj_list[node1] = list()

        if node2 not in adj_list:
            adj_list[node2] = list()

        adj_list[node1].append(node2)
        adj_list[node2].append(node1)

s1_adj_list = dict()
s2_adj_list = dict()

fill_adj_list(s1_adj_list, s1_graph_file)
fill_adj_list(s2_adj_list, s2_graph_file)


# calculate total degree of matching indexes (seeds)
BUCKET_SIZE = 500

def calculate_index_total_degree(index, adj_list):
    total_degree = 0

    for node in index:
        total_degree += len(adj_list[node])

    return total_degree

def add_to_histogram(histogram, value):
    histogram_index = value // BUCKET_SIZE

    while len(histogram) <= histogram_index:
        histogram.append(0)

    histogram[histogram_index] += 1

def print_histogram(histogram):
    for i in range(len(histogram)):
        print(i * BUCKET_SIZE, histogram[i])

s1_matching_histogram = list()
s2_matching_histogram = list()

for line in seeds_file:
    graphlet_id, s1_index_str, s2_index_str = re.split('[\s\t]', line.strip())
    s1_total_degree = calculate_index_total_degree(s1_index_str.split(','), s1_adj_list)
    s2_total_degree = calculate_index_total_degree(s2_index_str.split(','), s2_adj_list)
    add_to_histogram(s1_matching_histogram, s1_total_degree)
    add_to_histogram(s2_matching_histogram, s2_total_degree)

print('S1 MATCHING HISTOGRAM')
print_histogram(s1_matching_histogram)
print()
print('S2 MATCHING HISTOGRAM')
print_histogram(s2_matching_histogram)
print()


# calculate total degrees of all indexes
s1_all_histogram = list()
s2_all_histogram = list()

for line in s1_indexes_file:
    split_line = re.split('[\s\t]', line.strip())
    s1_index = split_line[1:]
    s1_total_degree = calculate_index_total_degree(s1_index, s1_adj_list)
    add_to_histogram(s1_all_histogram, s1_total_degree)

for line in s2_indexes_file:
    split_line = re.split('[\s\t]', line.strip())
    s2_index = split_line[1:]
    s2_total_degree = calculate_index_total_degree(s2_index, s2_adj_list)
    add_to_histogram(s2_all_histogram, s2_total_degree)

print('S1 ALL HISTOGRAM')
print_histogram(s1_all_histogram)
print()
print('S2 ALL HISTOGRAM')
print_histogram(s2_all_histogram)
