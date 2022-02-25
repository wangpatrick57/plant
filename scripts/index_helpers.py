# helps with file paths of cached blant output
PLANT_DIR = '/home/wangph1/plant'
CACHE_BASE_DIR = f'{PLANT_DIR}/data/seeding_cached_data'

def get_index_path(species, percent=0, orbit=0):
    if 'syeast' in species:
        lDEG = 3
    else:
        lDEG = 2

    return f'{CACHE_BASE_DIR}/blant_out/p{percent}-o{orbit}-{species}-lDEG{lDEG}.out'

def get_notopedge_index_path(species, percent=0, orbit=0, lDEG=2):
    return f'{CACHE_BASE_DIR}/special_blant_out/p{percent}-o{orbit}-{species}-lDEG{lDEG}-notopedge.out'

def read_index_file(index_file):
    index_list = []

    for curr_index_str in index_file:
        curr_index_str = curr_index_str.strip()
        assert len(curr_index_str.split(' ')) == k + 1, f'the line {curr_index_str} is not of size k{k}'
        curr_index = Index(curr_index_str)
        index_list.append(curr_index)

    return index_list
