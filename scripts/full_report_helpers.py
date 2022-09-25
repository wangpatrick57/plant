#!/pkg/python/3.7.4/bin/python3
import os
import sys
from all_helpers import *

def gtags_from_pairs(gtag_pairs):
    gtags = set()

    for gtag1, gtag2 in gtag_pairs:
        gtags.add(gtag1)
        gtags.add(gtag2)

    return sorted(list(gtags))

class FullReport:
    def __init__(self, algo):
        self._algo = algo
        self._idx_metrics = ['idx_vol', 'idx_time']
        self._seed_metrics = ['seed_vol', 'avg_nc', 'node_cov', 'perf_seed_vol', 'extr_vol', 'extr_nc']
        self._all_idx_metrics = dict()
        self._all_seed_metrics = dict()
        self._idx_fnames = []
        self._gtag_pairs = []

        for metric in self._idx_metrics:
            self._all_idx_metrics[metric] = dict()

        for metric in self._seed_metrics:
            self._all_seed_metrics[metric] = dict()

    def add_index_metrics(self, idx_fname, metrics):
        for metric_name, metric_val in zip(self._idx_metrics, metrics):
            self._all_idx_metrics[metric_name][idx_fname] = metric_val

        self._idx_fnames.append(idx_fname)

    def add_seed_metrics(self, gtag1, gtag2, metrics):
        key = (gtag1, gtag2)

        for metric_name, metric_val in zip(self._seed_metrics, metrics):
            self._all_seed_metrics[metric_name][key] = metric_val

        self._gtag_pairs.append(key)

    def __str__(self):
        s = f'{self._algo}\n'
        s += '\nINDEX\n'
        
        for metric_name, metric_dict in self._all_idx_metrics.items():
            s += f'{metric_name}: {metric_dict}\n'

        s += '\nSEED\n'

        for metric_name, metric_dict in self._all_seed_metrics.items():
            s += f'{metric_name}: {metric_dict}\n'

        return s

    def get_algo(self):
        return self._algo

    def format_metric(self, n):
        if n == None:
            return '---'
        if type(n) is float:
            return f'{n:.3f}'
        else:
            return str(n)

    def sheets_str(self):
        lines = ['INDEX METRICS']
        idx_fields = ['species'] + self._idx_metrics
        lines.append(','.join(idx_fields))

        for idx_fname in self._idx_fnames:
            data_items = [idx_fname]

            for metric_dict in self._all_idx_metrics.values():
                data_items.append(self.format_metric(metric_dict[idx_fname]))

            lines.append(','.join(data_items))

        lines.append('')
        lines.append('SEEDING METRICS')
        seed_fields = ['species_pair'] + self._seed_metrics
        lines.append(','.join(seed_fields))

        for gtag_pair in self._gtag_pairs:
            data_items = ['-'.join(gtag_pair)]

            for metric_dict in self._all_seed_metrics.values():
                data_items.append(self.format_metric(metric_dict[gtag_pair]))

            lines.append(','.join(data_items))

        return '\n'.join(lines)

def gen_all_indexes(gtags, algo, lDEG, overwrite=False):
    ps = []
    index_paths = dict()
    alph = True

    for gtag in gtags:
        p, index_path = run_blant(gtag, alph=alph, algo=algo, lDEG=lDEG, overwrite=overwrite)
        ps.append(p)
        index_paths[gtag] = index_path

    for p in ps:
        if p != None: # p will be None if overwrite is false and the index file already exists
            p.wait()

    return index_paths

def gen_all_indexes_sequential(gtags, algo, lDEG, overwrite=False):
    index_paths = dict()
    alph = True

    for gtag in gtags:
        p, index_path = run_blant(gtag, alph=alph, algo=algo, lDEG=lDEG, overwrite=overwrite)

        if p != None:
            p.wait()

        index_paths[gtag] = index_path

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
    graph1_path = get_graph_path(gtag1)
    graph2_path = get_graph_path(gtag2)
    g1_to_g2_orthologs = get_g1_to_g2_orthologs(gtag1, gtag2)
    all_seeds, seed_metrics, extr_metrics = raw_full_low_param_run(index1_path, graph1_path, index2_path, graph2_path, g1_to_g2_orthologs)
    all_metrics = [len(all_seeds)]
    all_metrics.extend(seed_metrics)
    all_metrics.extend(extr_metrics)
    all_metrics = tuple(all_metrics)
    full_report.add_seed_metrics(gtag1, gtag2, all_metrics)

def gen_and_store_all_seed_reports(full_report, index_paths, gtag_pairs):
    for gtag1, gtag2 in gtag_pairs:
        gen_and_store_seed_report(full_report, index_paths, gtag1, gtag2)

def gen_full_report(algo, gtag_pairs, lDEG):
    full_report = FullReport(algo)
    gtags = gtags_from_pairs(gtag_pairs)
    index_paths = gen_all_indexes(gtags, algo, lDEG)
    store_all_index_reports(full_report, index_paths)
    gen_and_store_all_seed_reports(full_report, index_paths, gtag_pairs)
    # run with P=1 C=5, storing seed_vol, avg_nc, node_cov, perf_seed_vol, extr_vol, extr_nc
    return full_report

if __name__ == '__main__':
    algo = sys.argv[1] if len(sys.argv) > 1 else None
    is_fast = True
    gtag_pairs = [('syeast0', 'syeast05'), ('syeast0', 'syeast10'), ('syeast0', 'syeast15'), ('syeast0', 'syeast20'), ('syeast0', 'syeast25')]
    lDEG = 1 if is_fast else 2
    full_report = gen_full_report(algo, gtag_pairs, lDEG)
    print('algo:', full_report.get_algo())
    print(full_report.sheets_str())
