import sys

def debug_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def convert_to_canonical_line(line):
    canon_id, g1, g2 = line.split(' ')
    canon_id = 'filler'
    g1 = ','.join(sorted(g1.split(',')))
    g2 = ','.join(sorted(g1.split(',')))
    return ' '.join([canon_id, g1, g2])

less_file = open(sys.argv[1], 'r')
more_file = open(sys.argv[2], 'r')

less_file_canon_lines = [convert_to_canonical_line(line) for line in less_file.readlines()]
less_file_canon_lines_set = set(less_file_canon_lines)
more_file_canon_lines = [convert_to_canonical_line(line) for line in more_file.readlines()]
more_file_canon_lines_set = set(more_file_canon_lines)

len1 = len(less_file_canon_lines)
len2 = len(less_file_canon_lines_set)
debug_print(f'less: {len1} and {len2}')
len1 = len(more_file_canon_lines)
len2 = len(more_file_canon_lines_set)
debug_print(f'more: {len1} and {len2}')

num_less_extra = 0

for line in less_file_canon_lines:
    if line not in more_file_canon_lines_set:
        num_less_extra += 1
        print(line)
    else:
        pass
        # print(line)

debug_print(f'less has {num_less_extra} extra lines that are not in more')
