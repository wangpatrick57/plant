def get_low_volume_pairs():
    return [('cat', 'human'), ('cat', 'sheep'), ('cow', 'human'), ('dog', 'human'), ('guineapig', 'human'), ('horse', 'human'), ('human', 'mouse'), ('human', 'pig'), ('human', 'rabbit'), ('human', 'rat'), ('mouse', 'sheep'), ('math_s0', 'math_s3'), ('math_s0', 'math_s5'), ('wiki_s0', 'wiki_s3'), ('wiki_s0', 'wiki_s5'), ('email_s0', 'email_s1'), ('email_s0', 'email_s3'), ('email_s0', 'email_s5'), ('college_s0', 'college_s3'), ('college_s0', 'college_s5'), ('alpha_s0', 'alpha_s3'), ('alpha_s0', 'alpha_s5')]

def get_dat_path(path):
    from file_helpers import get_data_path

    return get_data_path(f'zhi/dat/{path}')

def get_all_all_results():
    path = get_dat_path('all_all_results.dat')
    all_all_results = dict()

    with open(path, 'r') as f:
        for line in f:
            splitted = line.strip().split('\t')
            pair = splitted[0]
            convert = [int, float, int, int, int, float]
            results = [c(s) for c, s in zip(convert, splitted[1:])]
            all_all_results[pair] = results

    return all_all_results
