#!/bin/python3
import sys
from graph_helpers import *
from analysis_helpers import *
import os

CYTOMCS_DIR = f'{os.path.expanduser("~")}/faithmcs'
DEFAULT_PERTURBATION = 20
DEFAULT_MAX_NONIMPROVING = 20
DEFAULT_MAX_NUM_STEPS = 50

def get_sif_path(gtag):
    return '.'.join(get_graph_path(gtag).split('.')[:-1]) + '.sif'

def write_gtag_as_sif_file(gtag, overwrite=False):
    el = read_in_el(get_graph_path(gtag))
    out_path = get_sif_path(gtag)

    if overwrite or not os.path.exists(out_path):
        with open(out_path, 'w') as out_f:
            for node1, node2 in el:
                out_f.write(f'{node1} pp {node2}\n')
    else:
        print(f'using old sif file for {gtag}')

    return out_path

def build_faithmcs_package():
    r = subprocess.run(f'mvn compile -f {CYTOMCS_DIR}'.split(), capture_output=True)
    r.check_returncode()
    out = r.stdout.decode('utf-8')

    if 'Nothing to compile' not in out:
        r = subprocess.run(f'mvn package -f {CYTOMCS_DIR}'.split())
        r.check_returncode()
        
def get_cytomcs_alignment_path(gtag1, gtag2, perturbation=DEFAULT_PERTURBATION, max_nonimproving=DEFAULT_MAX_NONIMPROVING, max_num_steps=DEFAULT_MAX_NUM_STEPS):
    return get_data_path(f'cytomcs/cytomcs-{gtag1}-{gtag2}-p{perturbation}-i{max_nonimproving}-s{max_num_steps}.out')
            
def run_cytomcs_for_pair(gtag1, gtag2, perturbation=DEFAULT_PERTURBATION, max_nonimproving=DEFAULT_MAX_NONIMPROVING, max_num_steps=DEFAULT_MAX_NUM_STEPS, overwrite=False):
    def read_in_cytomcs_alignment(alignment_path, adj_set1, adj_set2):
        alignment = read_in_m2m(alignment_path, ignore_invalid_lines=True)
        alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
        assert_is_clean_alignment(alignment, adj_set1, adj_set2)
        return alignment

    sif_path1 = write_gtag_as_sif_file(gtag1)
    sif_path2 = write_gtag_as_sif_file(gtag2)
    alignment_path = get_cytomcs_alignment_path(gtag1, gtag2, perturbation=perturbation, max_nonimproving=max_nonimproving, max_num_steps=max_num_steps)

    if overwrite or not os.path.exists(alignment_path):
        build_faithmcs_package()
        r = subprocess.run(f'java -jar {CYTOMCS_DIR}/target/faithmcs-0.2.jar -p{perturbation / 100} -i{max_nonimproving} -s{max_num_steps} -o{alignment_path} {sif_path1} {sif_path2}'.split())
        r.check_returncode()
    else:
        print(f'using old alignment file for {gtag1}-{gtag2}')
        
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    alignment = read_in_cytomcs_alignment(alignment_path, adj_set1, adj_set2)
    size = len(alignment)
    nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
    s3 = get_s3(alignment, adj_set1, adj_set2)
    print(f'{gtag1}-{gtag2}', size, nc, s3)
            
if __name__ == '__main__':
    # write_gtag_as_sif_file(sys.argv[1])
    gtag1 = sys.argv[1]
    gtag2 = sys.argv[2]
    max_num_steps = sys.argv[3]
    run_cytomcs_for_pair(gtag1, gtag2, max_num_steps=max_num_steps, overwrite=True)
