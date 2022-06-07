#!/pkg/python/3.7.4/bin/python3
old_path = '/home/wangph1/BLANT/old'
new_path = '/home/wangph1/BLANT/new'
old_graphlets_without_id = []
new_graphlets_without_id = []

with open(old_path, 'r') as old_f:
    for line in old_f:
        splitted = line.strip().split()
        old_graphlets_without_id.append(tuple(splitted[1:]))

with open(new_path, 'r') as new_f:
    for line in new_f:
        splitted = line.strip().split()
        new_graphlets_without_id.append(tuple(splitted[1:]))

print(old_graphlets_without_id)
print(new_graphlets_without_id)
print('all old', len(old_graphlets_without_id))
print('all new', len(new_graphlets_without_id))
print('uniq old', len(set(old_graphlets_without_id)))
print('uniq new', len(set(new_graphlets_without_id)))
