#!/pkg/python/3.7.4/bin/python3
from all_helpers import *

pairs = get_paper_all_pairs()
print('\n'.join([f'{pair[0]}-{pair[1]}' for pair in pairs]))
print(len(pairs))
