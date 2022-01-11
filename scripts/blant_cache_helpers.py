# helps with file paths of cached blant output
PLANT_DIR = '/home/wangph1/plant'
CACHE_BASE_DIR = f'{PLANT_DIR}/data/seeding_cached_data/blant_out'

def get_index_path(species, percent=0, orbit=0, lDEG=2):
    return f'{CACHE_BASE_DIR}/p{percent}-o{orbit}-{species}-lDEG{lDEG}.out'
