import re
import math

def read_in_temporal_el(graph_path):
    with open(graph_path, 'r') as graph_file:
        tel = []

        for i, line in enumerate(graph_file):
            node1, node2, time = re.split('[\s\t]', line.strip())
            tel.append((node1, node2, time))

            if i % 600000 == 0: # simple print progress for stack overflow
                print(i)

        return tel

# start time is inclusive, end time is exclusive
def read_in_el_in_interval(graph_path, start_time, end_time):
    with open(graph_path, 'r') as graph_file:
        el = []

        for line in graph_file:
            node1, node2, time = re.split('[\s\t]', line.strip())

            if start_time <= time < end_time:
                el.append((node1, node2))

        return el

def map_density_over_time(tel, granularity=100):
    times = [int(row[2]) for row in tel]
    start_time = min(times)
    end_time = max(times) + 1
    tbins = [0] * granularity

    for time in times:
        tbin_num = math.floor((time - start_time) * granularity / (end_time - start_time))
        tbins[tbin_num] += 1

    for i, lines_in_this_range in enumerate(tbins):
        this_start_time = start_time + (end_time - start_time) * i / granularity
        print(this_start_time, lines_in_this_range)
