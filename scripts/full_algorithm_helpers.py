#!/pkg/python/3.7.4/bin/python3
from seeding_algorithm_core import *
from node_pair_extraction_helpers import *
from index_helpers import *
from odv_helpers import *
from ortholog_helpers import *
from patch_helpers import *
from index_validation_helpers import *
from graph_helpers import *

def get_gtag_run_info(gtag1, gtag2, g1_alph=True, g2_alph=True, algo='stairs', lDEG=2):
    g1_index_path = get_index_path(gtag1, alph=g1_alph, algo=algo, lDEG=lDEG)
    g2_index_path = get_index_path(gtag2, alph=g2_alph, algo=algo, lDEG=lDEG)
    g1_graph_path = get_graph_path(gtag1)
    g2_graph_path = get_graph_path(gtag2)
    g1_to_g2_orthologs = get_g1_to_g2_orthologs(gtag1, gtag2)
    return (g1_index_path, g1_graph_path, g2_index_path, g2_graph_path, g1_to_g2_orthologs)

def get_alphrev_gtag_run_infos(gtag1, gtag2, algo='stairs'):
    infos = []
    
    for g1_alph in [True, False]:
        for g2_alph in [True, False]:
            infos.append(get_gtag_run_info(gtag1, gtag2, g1_alph=g1_alph, g2_alph=g2_alph), algo=algo)

    return infos

def get_alphrev_strs():
    strs = []
    
    for g1_alph in [True, False]:
        for g2_alph in [True, False]:
            str_tup = ('alph' if g1_alph else 'rev', 'alph' if g2_alph else 'rev')
            strs.append(''.join(str_tup))

    return strs

def investigate_alphrev_effect(gtag1, gtag2):
    for alphrev_str, run_info in zip(get_alphrev_strs(), get_alphrev_gtag_run_infos(gtag1, gtag2)):
        seeds, seed_metrics, extr_metrics = raw_full_low_param_run(*run_info)
        print(f'{gtag1}-{gtag2} ({alphrev_str}): {len(seeds)} {seed_metrics} {extr_metrics}')

# low param means T=0, M=1, p=0, o=0 with only two index files (no combining)
def raw_full_low_param_run(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs, k=8, silent=False):
    raw_full_run(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs, k=k, settings=SeedingAlgorithmSettings(1, 0, 1), silent=silent)
    
def raw_full_run(s1_index_path, s1_graph_path, s2_index_path, s2_graph_path, s1_to_s2_orthologs, k=8, settings=SeedingAlgorithmSettings(), s1_odv_dir=None, s2_odv_dir=None, do_patch=True, silent=False):
    if not silent:
        print('starting run')
        
    if do_patch:
        s1_index = get_patched_index(k, s1_index_path, s1_graph_path, prox=1, target_num_matching=1)
        if not silent:
            print('got s1 patched index')
        s2_index = get_patched_index(k, s2_index_path, s2_graph_path, prox=1, target_num_matching=1)
        if not silent:
            print('got s2 patched index')
    else:
        s1_index = read_in_index(s1_index_path, k)
        s2_index = read_in_index(s2_index_path, k)

    seeds = find_seeds(s1_index, s2_index, settings=settings, g1_odv_dir=s1_odv_dir, g2_odv_dir=s2_odv_dir, print_progress=(not silent))
    return seeds

def get_all_metrics(seeds, g1_to_g2_ort, gtag1='', gtag2=''):
    from analysis_helpers import get_avg_size, get_seed_nc

    avg_size = get_avg_size(seeds)
    seed_nc = get_seed_nc(seeds, g1_to_g2_ort)
    seed_metrics = (avg_size, seed_nc)

    all_node_pairs = extract_node_pairs(seeds, ignore_deg_1=True, gtag1=gtag1, gtag2=gtag2)
    extr_vol = len(all_node_pairs)
    extr_nc = len(get_orthopairs_list(all_node_pairs, g1_to_g2_ort))
    extr_metrics = (extr_vol, extr_nc)

    return (seed_metrics, extr_metrics)

def seeds_to_str(seeds):
    lines = []
    
    for gid, entry1, entry2 in seeds:
        lines.append(f'{gid}\t{",".join(entry1)}\t{",".join(entry2)}')

    return '\n'.join(lines) + '\n'

# does everything. period.
def simplified_run_with_metrics(gtag1, gtag2, algo='stairs', settings=SeedingAlgorithmSettings(), overwrite=False, do_patch=True, silent=False):
    from file_helpers import file_exists
    from ortholog_helpers import get_g1_to_g2_orthologs
    from odv_helpers import ODVDirectory, ODV, get_odv_path, two_gtags_to_k

    seeds_path = get_seeds_path(gtag1, gtag2, algo=algo, settings=settings, do_patch=do_patch)

    if overwrite or not file_exists(seeds_path):
        if settings.sims_threshold == 0:
            s1_odv_dir = None
            s2_odv_dir = None
        else:
            ODV.set_weights_vars(two_gtags_to_k(gtag1, gtag2))
            s1_odv_dir = ODVDirectory(get_odv_path(gtag1, two_gtags_to_k(gtag1, gtag2)))
            s2_odv_dir = ODVDirectory(get_odv_path(gtag2, two_gtags_to_k(gtag1, gtag2)))
        
        seeds = raw_full_run(*get_gtag_run_info(gtag1, gtag2, algo=algo), settings=settings, s1_odv_dir=s1_odv_dir, s2_odv_dir=s2_odv_dir, do_patch=do_patch, silent=silent)
        seeds_str = seeds_to_str(seeds)
        write_to_file(seeds_str, seeds_path)
    else:
        if not silent:
            print(f'using old seeds file for {gtag1}-{gtag2}', file=sys.stderr)

        seeds = read_in_seeds(seeds_path)

    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    seed_metrics, extr_metrics = get_all_metrics(seeds, g1_to_g2_ort, gtag1=gtag1, gtag2=gtag2)
    return (seeds, seed_metrics, extr_metrics)

if __name__ == '__main__':
    from full_report_helpers import gen_all_indexes

    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    seeds, seed_metrics, extr_metrics = simplified_run_with_metrics(gtag1, gtag2)
    print(len(seeds), seed_metrics, extr_metrics)
