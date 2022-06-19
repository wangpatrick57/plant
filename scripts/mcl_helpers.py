#!/pkg/python/3.7.4/bin/python3
import sys

def get_nif_str(el):
    return('\n'.join([f'{node1}\t{node2}\t1' for node1, node2 in el]))

def gen_nif_file(gtag, overwrite=False):
    from graph_helpers import get_nif_path, get_marked_el
    from file_helpers import file_exists, write_to_file

    nif_path = get_nif_path(gtag)

    if overwrite or not file_exists(nif_path):
        marked_el = get_marked_el(gtag)
        write_to_file(get_nif_str(marked_el), nif_path)
    else:
        print(f'using old nif file for {gtag}', file=sys.stderr)

def gen_odv_ort_file(gtag1, gtag2, overwrite=False, notes=''):
    from graph_helpers import gtag_to_mark, read_in_adj_set, get_graph_path
    from odv_helpers import get_odv_orthologs, odv_ort_to_str, get_odv_ort_path, two_gtags_to_k, two_gtags_to_n, ODV, odv_ort_to_nodes
    from file_helpers import file_exists, write_to_file
    from analysis_helpers import get_deg_distr, deg_distr_to_str

    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    ODV.set_weights_vars(k)
    ort_path = get_odv_ort_path(gtag1, gtag2, k, n, notes=notes)

    if overwrite or not file_exists(ort_path):
        odv_ort = get_odv_orthologs(gtag1, gtag2, k, n)

        # PAT DEBUG
        nodes = odv_ort_to_nodes(odv_ort, True)
        deg_distr = get_deg_distr(nodes, read_in_adj_set(get_graph_path(gtag1)))
        write_to_file(deg_distr_to_str(deg_distr), f'{ort_path}.dgds')
        # DEBUG END

        mark1 = gtag_to_mark(gtag1)
        mark2 = gtag_to_mark(gtag2)
        ort_str = odv_ort_to_str(odv_ort, mark1, mark2)
        write_to_file(ort_str, ort_path)
    else:
        print(f'using old odv ort file for {gtag1}-{gtag2}', file=sys.stderr)

def copy_to_out(gtag1, gtag2, notes=''):
    from bash_helpers import run_outsend
    from graph_helpers import get_nif_path
    from odv_helpers import get_odv_ort_path, two_gtags_to_k, two_gtags_to_n

    nif_path1 = get_nif_path(gtag1)
    nif_path2 = get_nif_path(gtag2)
    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    ort_path = get_odv_ort_path(gtag1, gtag2, k, n, notes=notes)
    run_outsend(nif_path1)
    run_outsend(nif_path2)
    run_outsend(ort_path)

def get_mcl_out_fname(gtag1, gtag2, k, n, notes=''):
    base = f'{gtag1}-{gtag2}-k{k}-n{n}'

    if notes != '':
        base += f'-{notes}'

    return f'{base}.txt'

def get_mcl_out_path(gtag1, gtag2, k, n, notes=''):
    from file_helpers import get_data_path
    return get_data_path(f'mcl/{get_mcl_out_fname(gtag1, gtag2, k, n, notes=notes)}')

def take_from_out(gtag1, gtag2, notes=''):
    from bash_helpers import run_outtake
    from odv_helpers import two_gtags_to_k, two_gtags_to_n

    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    out_fname = get_mcl_out_fname(gtag1, gtag2, k, n, notes=notes)
    here_path = get_mcl_out_path(gtag1, gtag2, k, n, notes=notes)
    run_outtake(out_fname, here_path) # note: the out here means the output file of mcl, while the out param of run_outtake refers to the remote git repo called "out" (which is named vmcopy lol)

def evaluate_alignment(gtag1, gtag2, notes=''):
    from node_pair_extraction_helpers import MarkedSelfOrthos, read_in_slashes_m2m, extract_node_pairs_from_m2m, get_orthopairs_list, get_g1_to_g2_orthologs
    from odv_helpers import two_gtags_to_k, two_gtags_to_n
    from file_helpers import write_to_file

    k = two_gtags_to_k(gtag1, gtag2)
    n = two_gtags_to_n(gtag1, gtag2)
    out_path = get_mcl_out_path(gtag1, gtag2, k, n, notes=notes)
    m2m_pairs = read_in_slashes_m2m(out_path)
    node_pairs = extract_node_pairs_from_m2m(m2m_pairs)
    node_pairs_str = '\n'.join(f'{node1}\t{node2}' for node1, node2 in node_pairs)
    orthologs = get_g1_to_g2_orthologs(gtag1, gtag2)
    orthopairs = get_orthopairs_list(node_pairs, orthologs)
    return len(orthopairs), len(node_pairs)

def prepare_mcl(gtag1, gtag2, notes=''):
    from bash_helpers import run_orca_for_gtag

    gen_nif_file(gtag1)
    gen_nif_file(gtag2)
    run_orca_for_gtag(gtag1)
    run_orca_for_gtag(gtag2)
    gen_odv_ort_file(gtag1, gtag2, notes=notes)

def process_mcl(gtag1, gtag2, notes=''):
    num_ort, num_pairs = evaluate_alignment(gtag1, gtag2, notes=notes)
    print(f'{num_ort} / {num_pairs}')

def full_local_run_mcl(gtag1, gtag2, notes=''):
    from bash_helpers import run_align_mcl

    prepare_mcl(gtag1, gtag2, notes=notes)
    p = run_align_mcl(gtag1, gtag2, notes=notes)

    if p != None:
        p.wait()

    process_mcl(gtag1, gtag2, notes=notes)

if __name__ == '__main__':
    mode = sys.argv[1]
    gtag1 = sys.argv[2]
    gtag2 = sys.argv[3]
    notes = sys.argv[4] if len(sys.argv) > 4 else ''

    if mode == 'prep':
        prepare_mcl(gtag1, gtag2, notes=notes)
        copy_to_out(gtag1, gtag2, notes=notes)
    elif mode == 'proc':
        take_from_out(gtag1, gtag2, notes=notes)
        process_mcl(gtag1, gtag2, notes=notes)
    elif mode == 'full':
        full_local_run_mcl(gtag1, gtag2, notes=notes)
    else:
        print('USAGE: mcl_helpers.py gtag1 gtag2 mode, where mode is prep or proc')
