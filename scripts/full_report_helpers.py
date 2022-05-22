#!/pkg/python/3.7.4/bin/python3
import os
from all_helpers import *

# TRUE_BASE_PAIRS = [('mouse', 'human'), ('mouse', 'rat'), ('syeast0', 'syeast15'), ('alpha1', 'alpha2'), ('math1', 'math2'), ('email1', 'email2'), ('gnutellafour_10v1', 'gnutellafour_10v2'), ('hepph_5v1', 'hepph_5v2')]
BASE_PAIRS = [('syeast0', 'syeast15'), ('email1', 'email2')]

def get_all_gtags():
    all_gtags = set()

    for gtag1, gtag2 in BASE_PAIRS:
        all_gtags.add(gtag1)
        all_gtags.add(gtag2)

    return list(all_gtags)

ALL_GTAGS = get_all_gtags()

class FullReport:
    def __init__(self, algo):
        self._algo = algo
        self._idx_metrics = ['idx_vol', 'idx_time']
        self._seed_metrics = ['seed_vol', 'avg_nc', 'node_cov', 'perf_seed_vol', 'extr_vol', 'extr_nc']
        self._all_idx_metrics = dict()
        self._all_seed_metrics = dict()

        for metric in self._idx_metrics:
            self._all_idx_metrics[metric] = dict()

        for metric in self._seed_metrics:
            self._all_seed_metrics[metric] = dict()

    def add_index_metrics(self, idx_fname, metrics):
        for metric_name, metric_val in zip(self._idx_metrics, metrics):
            self._all_idx_metrics[metric_name][idx_fname] = metric_val

    def add_seed_metrics(self, gtag1, gtag2, metrics):
        key = (gtag1, gtag2)

        for metric_name, metric_val in zip(self._seed_metrics, metrics):
            self._all_seed_metrics[metric_name][key] = metric_val

    def __str__(self):
        s = f'{self._algo}\n'
        s += '\nINDEX\n'
        
        for metric_name, metric_dict in self._all_idx_metrics.items():
            s += f'{metric_name}: {metric_dict}\n'

        s += '\nSEED\n'

        for metric_name, metric_dict in self._all_seed_metrics.items():
            s += f'{metric_name}: {metric_dict}\n'

        return s

    def sheets_str(self):
        pass

def gen_all_indexes(algo):
    ps = []
    index_paths = dict()

    for gtag in ALL_GTAGS:
        p, index_path = run_blant(gtag, algo=algo, lDEG=1)
        ps.append(p)
        index_paths[gtag] = index_path

    for p in ps:
        p.wait()

    return index_paths

def extract_index_metrics(index_path):
    with open(index_path, 'r') as index_file:
        idx_vol = len(index_file.readlines())

    with open(f'{index_path}.time', 'r') as index_time_file:
        lines = index_time_file.readlines()
        time_line = lines[1]
        after_m = time_line.split('m')[1]
        time_str = after_m.split('s')[0]
        idx_time = float(time_str)

    return idx_vol, idx_time

def store_index_report(full_report, index_path):
    idx_vol, idx_time = extract_index_metrics(index_path)
    full_report.add_index_metrics(os.path.basename(index_path), (idx_vol, idx_time))

def store_all_index_reports(full_report, index_paths):
    for index_path in index_paths.values():
        store_index_report(full_report, index_path)

def gen_and_store_seed_report(full_report, index_paths, gtag1, gtag2):
    index1_path = index_paths[gtag1]
    index2_path = index_paths[gtag2]
    graph1_path = get_gtag_graph_path(gtag1)
    graph2_path = get_gtag_graph_path(gtag2)
    g1_to_g2_orthologs = get_g1_to_g2_orthologs(gtag1, gtag2)
    all_seeds, avg_nc, node_cov = low_param_one_run(index1_path, graph1_path, index2_path, graph2_path, g1_to_g2_orthologs)
    seed_vol = len(all_seeds)
    full_report.add_seed_metrics(gtag1, gtag2, (seed_vol, avg_nc, node_cov, 0, 0, 0))

def gen_and_store_all_seed_reports(full_report, index_paths):
    for gtag1, gtag2 in BASE_PAIRS:
        gen_and_store_seed_report(full_report, index_paths, gtag1, gtag2)

def gen_full_report(algo):
    full_report = FullReport(algo)
    index_paths = gen_all_indexes(algo)
    store_all_index_reports(full_report, index_paths)
    gen_and_store_all_seed_reports(full_report, index_paths)
    # run with P=1 C=5, storing seed_vol, avg_nc, node_cov, perf_seed_vol, extr_vol, extr_nc
    return full_report

if __name__ == '__main__':
    print(str(gen_full_report(None)))
