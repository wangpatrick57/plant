#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import subprocess

def run_blant(gtag, lDEG=2, alph=True):
    graph_path = get_gtag_graph_path(gtag)
    out_path = get_index_path(gtag)
    subprocess.call(f'run_blant_default_custom.sh {graph_path} {lDEG} {alph} {out_path}', shell=True)
