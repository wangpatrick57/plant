#!/pkg/python/3.7.4/bin/python3
from all_helpers import *
import subprocess

def bool_conv(b):
    return 1 if b else 0

def run_blant(gtag, lDEG=2, alph=True, algo=None):
    assert alph != None # alph can't be None because we need a different .sh script for that
    graph_path = get_gtag_graph_path(gtag)
    out_path = get_index_path(gtag, lDEG=lDEG, alph=alph, algo=algo)
    cmd = f'run_blant_default_custom.sh {graph_path} {lDEG} {bool_conv(alph)} {out_path}'
    p = subprocess.Popen(cmd.split())
    return p, out_path
