#!/bin/python3
class IndexSelector:
    CACHE_BASE_DIR = '/home/wangph1/plant/data/seeding_cached_data'

    def __init__(self, by_blant_settings=None, by_cache_relative_path=None, by_absolute_path=None):
        num_not_none = 0

        for setting in [by_blant_settings, by_cache_relative_path, by_absolute_path]:
            if setting != None:
                num_not_none += 1

        assert num_not_none == 1, 'you must use exactly one selector'

        if by_blant_settings != None:
            species = by_blant_settings['species']
            percent = by_blant_settings['percent'] if 'percent' in by_blant_settings else 0
            orbit = by_blant_settings['orbit'] if 'orbit' in by_blant_settings else 0
            ldeg = by_blant_settings['ldeg'] if 'ldeg' in by_blant_settings else IndexSelector.get_default_ldeg(species)
            self._path = f'{IndexSelector.CACHE_BASE_DIR}/blant_out/p{percent}-o{orbit}-{species}-lDEG{ldeg}.out'
        elif by_cache_relative_path != None:
            self._path = f'{IndexSelector.CACHE_BASE_DIR}/{by_cache_relative_path}'
        elif by_absolute_path != None:
            self._path = by_absolute_path
        else:
            raise AssertionError('above assertion written wrong')

    def get_path(self):
        return self._path

    @staticmethod
    def get_default_ldeg(species):
        if 'syeast' in species:
            return 3
        else:
            return 2

if __name__ == '__main__':
    by_blant_settings = {'species': 'mouse', 'orbit': 3}
    index_selector = IndexSelector(by_blant_settings=by_blant_settings)
    print(index_selector.get_path())
