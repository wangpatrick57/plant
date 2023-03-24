#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import sys

def get_dds_list(gtags, delim=',', scale_deg=False, scale_count=False):
    dds_list = []
    
    for gtag in gtags:
        adj_set = read_in_adj_set(get_graph_path(gtag))
        deg_distr = get_deg_distr(adj_set.keys(), adj_set)

        if scale_deg or scale_count:
            max_deg = max(deg_distr.keys())
            max_count = max(deg_distr.values())
            scaled_deg_distr = dict()

            for deg, count in deg_distr.items():
                scaled_deg = deg / max_deg * 100 if scale_deg else deg
                scaled_count = count / max_count * 100 if scale_count else count
                scaled_deg_distr[scaled_deg] = scaled_count

            deg_distr = scaled_deg_distr
        
        dds = distr_to_str(deg_distr, 'deg', delim=delim)
        dds_list.append(dds)

    return dds_list

def print_human_readable(gtags, delim=',', scale_deg=False, scale_count=False):
    dds_list = get_dds_list(gtags, delim=delim, scale_deg=scale_deg, scale_count=scale_count)
    print((delim * 3).join(gtags))
    ddsl_list = [dds.split('\n') for dds in dds_list]
    max_len = max([len(ddsl) for ddsl in ddsl_list])

    for line_i in range(max_len):
        for gtag_i, ddsl in enumerate(ddsl_list):
            if line_i >= len(ddsl):
                print(delim * 2, end='')
            else:
                print(ddsl[line_i] + delim, end='')

            if gtag_i != len(ddsl_list) - 1:
                print(delim, end='')

        print()

def print_gnuplot_dat(gtags, delim=',', scale_deg=False, scale_count=False):
    dds_list = get_dds_list(gtags, delim=delim, scale_deg=scale_deg, scale_count=scale_count)
    ddsl_list = [dds.split('\n') for dds in dds_list]
    max_len = max([len(ddsl) for ddsl in ddsl_list])

    for line_i in range(max_len):
        if line_i == 0:
            continue
        
        for gtag_i, ddsl in enumerate(ddsl_list):
            if line_i >= len(ddsl):
                print(ddsl[-1], end='') # just print the last data point as a filler
            else:
                print(ddsl[line_i], end='')

            if gtag_i != len(ddsl_list) - 1:
                print(delim * 2, end='')

        print()
        
if __name__ == '__main__':
    # gtags = get_tprl_gtags()
    base = sys.argv[1]
    gtags = [f'{base}_s0', f'{base}_s1', f'{base}_s3', f'{base}_s5']
    print_gnuplot_dat(gtags, delim='\t', scale_deg=False, scale_count=False)
