from low_seed_investigator import *

def main():
    rat_og_edge_set = get_edge_set('/home/sana/Jurisica/IID/networks/IIDrat.el')
    to_remove_edge_set = get_edge_set('/home/wangph1/plant/networks/low_investigation/rat_200_4_removed.el')
    to_remove_edge_set = set(list(to_remove_edge_set)[150:200])
    edge_set_to_print = rat_og_edge_set - to_remove_edge_set

    print(len(rat_og_edge_set))
    print(len(to_remove_edge_set))
    print(len(edge_set_to_print))

    print('\n'.join(['\t'.join(edge_str.split(',')) for edge_str in edge_set_to_print]), file=sys.stderr)

if __name__ == '__main__':
    main()
