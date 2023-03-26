#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

gtag1 = sys.argv[1]
gtag2 = sys.argv[2]
notes = sys.argv[3]
k = two_gtags_to_k(gtag1, gtag2)
n = two_gtags_to_n(gtag1, gtag2)
mcl_out_path = get_mcl_out_path(gtag1, gtag2, k, n, notes=notes)
alignments = read_in_slashes_alignments(mcl_out_path)
alignments = unmarked_anthill(alignments)
alignments_str = alignments_to_str(alignments)
out_path = f'{gtag1}-{gtag2}-mclseeds.txt'
write_to_file(alignments_str, out_path)
