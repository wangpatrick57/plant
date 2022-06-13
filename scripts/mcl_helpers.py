#!/pkg/python/3.7.4/bin/python3
import sys

N = 5

def get_nif_str(el):
    return('\n'.join([f'{node1}\t{node2}\t1' for node1, node2 in el]))

def gen_nif_file(gtag, overwrite=False):
    from graph_helpers import get_nif_path, get_graph_path, read_in_el
    from file_helpers import file_exists, write_to_file

    nif_path = get_nif_path(gtag)

    if overwrite or not file_exists(nif_path):
        path = get_graph_path(gtag)
        el = read_in_el(path)
        write_to_file(get_nif_str(el), nif_path)
    else:
        print(f'using old nif file for {gtag}', file=sys.stderr)

def two_gtags_to_k(gtag1, gtag2):
    from odv_helpers import gtag_to_k

    assert gtag_to_k(gtag1) == gtag_to_k(gtag2)
    k = gtag_to_k(gtag1)
    return k

def gen_odv_ort_file(gtag1, gtag2, overwrite=False):
    from graph_helpers import gtag_to_mark
    from odv_helpers import get_odv_orthologs, odv_ort_to_str, get_odv_ort_path
    from file_helpers import file_exists, write_to_file

    k = two_gtags_to_k(gtag1, gtag2)
    ort_path = get_odv_ort_path(gtag1, gtag2, k, N)

    if overwrite or not file_exists(ort_path):
        odv_ort = get_odv_orthologs(gtag1, gtag2, N, k)
        mark1 = gtag_to_mark(gtag1)
        mark2 = gtag_to_mark(gtag2)
        ort_str = odv_ort_to_str(odv_ort, mark1, mark2)
        write_to_file(ort_str, ort_path)
    else:
        print(f'using old odv ort file for {gtag1}-{gtag2}', file=sys.stderr)

def copy_to_out(gtag1, gtag2):
    from bash_helpers import run_outsend
    from graph_helpers import get_nif_path
    from odv_helpers import get_odv_ort_path

    nif_path1 = get_nif_path(gtag1)
    nif_path2 = get_nif_path(gtag2)
    k = two_gtags_to_k(gtag1, gtag2)
    ort_path = get_odv_ort_path(gtag1, gtag2, k, N)
    run_outsend(nif_path1)
    run_outsend(nif_path2)
    run_outsend(ort_path)

def full_prepare_mcl(gtag1, gtag2):
    from bash_helpers import run_orca_for_gtag

    gen_nif_file(gtag1)
    gen_nif_file(gtag2)
    run_orca_for_gtag(gtag1)
    run_orca_for_gtag(gtag2)
    gen_odv_ort_file(gtag1, gtag2)
    copy_to_out(gtag1, gtag2)

if __name__ == '__main__':
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    full_prepare_mcl(gtag1, gtag2)
