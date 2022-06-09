#!/pkg/python/3.7.4/bin/python3
from graph_helpers import *
from index_helpers import *
import subprocess

def bool_conv(b):
    return 1 if b else 0

def run_blant(gtag, lDEG=2, alph=True, algo=None, overwrite=False):
    assert alph != None # alph can't be None because we need a different .sh script for that
    graph_path = get_graph_path(gtag)
    out_path = get_index_path(gtag, lDEG=lDEG, alph=alph, algo=algo)

    if overwrite or not file_exists(out_path):
        common_settings = f'{graph_path} {lDEG} {bool_conv(alph)} {out_path}'

        if algo == None:
            cmd = f'run_blant_default_custom.sh {common_settings}'
        else:
            cmd = f'run_blant_default_custom_algo.sh {algo} {common_settings}'

        p = subprocess.Popen(cmd.split())
    else:
        p = None

    return p, out_path

def run_orca(k, el_path):
    cmd = f'orca.sh {k} {el_path}'
    p = subprocess.run(cmd.split(), capture_output=True)
    return p

if __name__ == '__main__':
    run_blant('tester', algo='a')
