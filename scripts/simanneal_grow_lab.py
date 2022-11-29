#!/bin/python3
from all_helpers import *

# all functions use certain global variables defined in if __name__ == '__main__'
def e2e(k):
    sagrow = SimAnnealGrow(blocks, adj_set1, adj_set2, p_func=p_func, s3_threshold=s3_threshold)
    alignment = sagrow.run(k)
    alignment = get_clean_alignment(alignment, adj_set1, adj_set2)
    size = len(alignment)
    nc = get_alignment_nc(alignment, g1_to_g2_ort, adj_set1, adj_set2)
    s3 = get_s3(alignment, adj_set1, adj_set2)
    print('generated', size, nc, s3, file=sys.stderr)
    return (size, nc, s3)

def get_idstr():
    return f'{gtag1}-{gtag2} {algo} {p_func} s3_thresh={s3_threshold}'

def same_k_many_runs(k, num_runs):
    print(f'{num_runs} runs on k={k}', get_idstr())
    results = [e2e(k) for _ in range(num_runs)]

    print(f'{num_runs} runs on k={k}', get_idstr())
    print('run', 'size', 'nc', 's3')
            
    for i, result in enumerate(results, 1):
        print(i, ' '.join(map(str, result)))

def multiple_k_many_runs(k_list, num_runs_per_k):
    print(f'{num_runs_per_k} runs each for k={k_list}', get_idstr())
    results = [[e2e(k) for _ in range(num_runs_per_k)] for k in k_list]

    print(f'{num_runs_per_k} runs each for k={k_list}', get_idstr())
    print('k', 'mean_size mean_nc mean_s3', ' '.join([f'size_{n} nc_{n} s3_{n}' for n in range(1, num_runs_per_k + 1)]))
            
    for k, result in zip(k_list, results):
        mean_size = sum([run[0] for run in result]) / len(result)
        mean_nc = sum([run[1] for run in result]) / len(result)
        mean_s3 = sum([run[2] for run in result]) / len(result)
        print(k, mean_size, mean_nc, mean_s3, ' '.join([' '.join(map(str, run)) for run in result]))

# all the functions use these same global variables
if __name__ == '__main__':
    gtag1 = 'mouse'
    gtag2 = 'rat'
    algo = 'stairs'
    p_func = ALWAYS_P_FUNC
    s3_threshold = 0.8
    
    adj_set1 = read_in_adj_set(get_graph_path(gtag1))
    adj_set2 = read_in_adj_set(get_graph_path(gtag2))
    g1_to_g2_ort = get_g1_to_g2_orthologs(gtag1, gtag2)
    
    blocks = get_mcl_blocks(gtag1, gtag2, 5, 0.6, 'no1')
    result = e2e(10000)
    print(result)
