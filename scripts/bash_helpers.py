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
        print(f'using old index file for {gtag}', file=sys.stderr)

    return p, out_path

def run_outsend(path):
    cmd = f'outsend {path}'
    subprocess.run(cmd.split())

def run_orca_raw(k, el_path):
    cmd = f'orca.sh {k} {el_path}'
    p = subprocess.run(cmd.split(), capture_output=True)
    return p

def run_orca_for_gtag(gtag, overwrite=False):
    from graph_helpers import get_graph_path
    from file_helpers import write_to_file, file_exists
    from odv_helpers import get_odv_path, gtag_to_k
    k = gtag_to_k(gtag)
    odv_path = get_odv_path(gtag, k)

    if overwrite or not file_exists(odv_path):
        el_path = get_graph_path(gtag)
        p = run_orca_raw(k, el_path)
        out_str = p.stdout.decode()
        write_to_file(out_str, odv_path)
    else:
        print(f'using old odv file for {gtag}', file=sys.stderr)

if __name__ == '__main__':
    run_orca_for_gtag('tester')
