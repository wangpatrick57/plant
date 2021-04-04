orbits_file = open('/home/wangph1/plant/data/patching/orbits_mouse_rat_611.txt', 'r')
patched_ids_file = open('/home/wangph1/plant/data/patching/ids_mouse_rat_611.txt', 'r')

ONLY_M1 = False
is_m1s = []
canon_ids = []
patch_ids = []

for line in orbits_file:
    canon_id, is_m1 = line.strip().split(' ')
    is_m1 = bool(int(is_m1))
    is_m1s.append(is_m1)
    canon_ids.append(canon_id)

for line in patched_ids_file:
    patch_id = line.strip()
    patch_ids.append(patch_id)

canon_to_patch = dict()
patch_to_canon = dict()

assert len(is_m1s) == len(canon_ids) == len(patch_ids)

for i in range(len(is_m1s)):
    is_m1 = is_m1s[i]

    if ONLY_M1 and not is_m1:
        continue

    canon_id = canon_ids[i]
    patch_id = patch_ids[i]

    if canon_id not in canon_to_patch:
        canon_to_patch[canon_id] = set()

    if patch_id not in patch_to_canon:
        patch_to_canon[patch_id] = set()

    canon_to_patch[canon_id].add(patch_id)
    patch_to_canon[patch_id].add(canon_id)

for canon_id, corr_patch_ids in canon_to_patch.items():
    if len(corr_patch_ids) > 1:
        print(f'the patch ids {" === ".join(corr_patch_ids)} correspond to {canon_id}')

for patch_id, corr_canon_ids in patch_to_canon.items():
    if len(corr_canon_ids) > 1:
        print(f'the canon ids {" === ".join(corr_canon_ids)} correspond to {patch_id}')

print(f'{len(canon_to_patch)} canon_ids, {len(patch_to_canon)} patch_ids')
