# helps with file paths of cached blant output
PLANT_DIR = '/home/wangph1/plant'
CACHE_BASE_DIR = f'{PLANT_DIR}/data/seeding_cached_data'

def get_index_path(species, percent=0, orbit=0, lDEG=2):
    return f'{CACHE_BASE_DIR}/blant_out/p{percent}-o{orbit}-{species}-lDEG{lDEG}.out'

def get_notopedge_index_path(species, percent=0, orbit=0, lDEG=2):
    return f'{CACHE_BASE_DIR}/special_blant_out/p{percent}-o{orbit}-{species}-lDEG{lDEG}-notopedge.out'
