#!/bin/python3
import subprocess
import random

TESTING1 = 'testing1'
TESTING2 = 'testing2'
TESTING1_BLANT_OUT_PATH = '/home/wangph1/data/seeding_cached_data/blant_out/p0-o0-testing1-stairs-lDEG2-alph.out'
TESTING2_BLANT_OUT_PATH = '/home/wangph1/data/seeding_cached_data/blant_out/p0-o0-testing2-stairs-lDEG2-alph.out'
TESTING1_ODV_OUT_PATH = '/home/wangph1/data/odv/testing1-k4.odv'
TESTING2_ODV_OUT_PATH = '/home/wangph1/data/odv/testing2-k4.odv'
SEEDS_PATH = '/home/wangph1/data/seeds/testing1-testing2_stairs_mi1_st-0.95_patchTrue.seeds'

def get_num_lines(path):
    p = subprocess.run(f'wc -l {path}'.split(), capture_output=True)
    p.check_returncode()
    stdout = p.stdout.decode('utf-8')
    num_lines = int(stdout.split(' ')[0])
    return num_lines

def assert_num_lines(path, expected):
    num_lines = get_num_lines(path)
    assert num_lines == expected, f'{path} has {num_lines}, when {expected} was expected'

# clean files
p = subprocess.run(f'rm {TESTING1_BLANT_OUT_PATH}'.split())
p = subprocess.run(f'rm {TESTING2_BLANT_OUT_PATH}'.split())
p = subprocess.run(f'rm {TESTING1_ODV_OUT_PATH}'.split())
p = subprocess.run(f'rm {TESTING2_ODV_OUT_PATH}'.split())

# run blant for both
p = subprocess.run(f'run_blant_tool.py {TESTING1} stairs'.split())
p.check_returncode()
assert_num_lines(TESTING1_BLANT_OUT_PATH, 2493)
print('testing1 blant good')

p = subprocess.run(f'run_blant_tool.py {TESTING2} stairs'.split())
p.check_returncode()
assert_num_lines(TESTING2_BLANT_OUT_PATH, 5240)
print('testing2 blant good')

# run ODV for both
p = subprocess.run(f'run_orca.py {TESTING1} 4'.split())
p.check_returncode()
assert_num_lines(TESTING1_ODV_OUT_PATH, 377)
print('testing1 odv good')

p = subprocess.run(f'run_orca.py {TESTING2} 4'.split())
p.check_returncode()
assert_num_lines(TESTING2_ODV_OUT_PATH, 376)
print('testing2 odv good')

# run seeds
p = subprocess.run(f'run_seeds.py {TESTING1} {TESTING2} -m1 -s-0.95'.split())
p.check_returncode()
assert_num_lines(SEEDS_PATH, 45)
print('seeds good')

# run SAG
p = subprocess.run(f'run_sag.py {TESTING1} {TESTING2} 1 -0.95'.split())
p.check_returncode()