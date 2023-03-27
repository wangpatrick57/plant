#!/bin/python3
import subprocess
import random
from index_helpers import get_index_path
from odv_helpers import get_odv_path, two_gtags_to_k, two_gtags_to_n
from file_helpers import get_seeds_path
from seeding_algorithm_core import SeedingAlgorithmSettings
from mcl_helpers import get_mcl_out_path, clean_mcl

TESTING1 = 'testing1'
TESTING2 = 'testing2'
MAX_INDICES = 1
SIMS_THRESHOLD = -0.99
LDEG = 2
ALPH = True
ORT_ALGO = 'no1'
ODV_K = two_gtags_to_k(TESTING1, TESTING2)
ODV_N = two_gtags_to_n(TESTING1, TESTING2)
SEEDING_ALGORITHM_SETTINGS = SeedingAlgorithmSettings(max_indices=MAX_INDICES, sims_threshold=SIMS_THRESHOLD)
TESTING1_BLANT_OUT_PATH = get_index_path(TESTING1, lDEG=LDEG, alph=ALPH, algo=None)
TESTING2_BLANT_OUT_PATH = get_index_path(TESTING2, lDEG=LDEG, alph=ALPH, algo=None)
TESTING1_ODV_OUT_PATH = get_odv_path(TESTING1, ODV_K)
TESTING2_ODV_OUT_PATH = get_odv_path(TESTING2, ODV_K)
SEEDS_PATH = get_seeds_path(TESTING1, TESTING2, algo=None, settings=SEEDING_ALGORITHM_SETTINGS)
MCL_PATH = get_mcl_out_path(TESTING1, TESTING2, ODV_K, ODV_N, notes=ORT_ALGO)

def get_num_lines(path):
    p = subprocess.run(f'wc -l {path}'.split(), capture_output=True)
    p.check_returncode()
    stdout = p.stdout.decode('utf-8')
    num_lines = int(stdout.split(' ')[0])
    return num_lines

def assert_num_lines(path, expected):
    num_lines = get_num_lines(path)
    assert num_lines == expected, f'{path} has {num_lines}, when {expected} was expected'

def clean_files():
    p = subprocess.run(f'rm {TESTING1_BLANT_OUT_PATH}'.split(), capture_output=True)
    p = subprocess.run(f'rm {TESTING2_BLANT_OUT_PATH}'.split(), capture_output=True)
    p = subprocess.run(f'rm {TESTING1_ODV_OUT_PATH}'.split(), capture_output=True)
    p = subprocess.run(f'rm {TESTING2_ODV_OUT_PATH}'.split(), capture_output=True)
    p = subprocess.run(f'rm {SEEDS_PATH}'.split(), capture_output=True)
    clean_mcl(TESTING1, TESTING2, ORT_ALGO) # there are a lot of MCL files to clean, so I'm going to reuse the existing function that does so

# clean files first
clean_files()

# run blant for both
p = subprocess.run(f'run_blant.py {TESTING1}'.split())
p.check_returncode()
assert_num_lines(TESTING1_BLANT_OUT_PATH, 1117)
print('testing1 blant good')

p = subprocess.run(f'run_blant.py {TESTING2}'.split())
p.check_returncode()
assert_num_lines(TESTING2_BLANT_OUT_PATH, 1556)
print('testing2 blant good')

# run ODV for both
p = subprocess.run(f'run_orca.py {TESTING1}'.split())
p.check_returncode()
assert_num_lines(TESTING1_ODV_OUT_PATH, 377)
print('testing1 odv good')

p = subprocess.run(f'run_orca.py {TESTING2}'.split())
p.check_returncode()
assert_num_lines(TESTING2_ODV_OUT_PATH, 376)
print('testing2 odv good')

# run seeds
p = subprocess.run(f'run_seeds.py {TESTING1} {TESTING2} -m{MAX_INDICES} -s{SIMS_THRESHOLD}'.split())
p.check_returncode()
assert_num_lines(SEEDS_PATH, 7)
print('seeds good')

# run SAG
p = subprocess.run(f'run_sag.py {TESTING1} {TESTING2} -m{MAX_INDICES} -s{SIMS_THRESHOLD}'.split())
p.check_returncode()
print('sag good')

# run AlignMCL
p = subprocess.run(f'run_mcl.py {TESTING1} {TESTING2} -o{ORT_ALGO}'.split())
p.check_returncode()
assert_num_lines(MCL_PATH, 89)
print('mcl good')

# clean files at the end as well
clean_files()

# final
print()
print('=======================')
print('END2END TESTS SUCCEEDED')
print('=======================')