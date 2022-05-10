#!/pkg/python/3.7.4/bin/python3
bases = ['alpha', 'reddit', 'college', 'ubuntu']
adds = ['0', '1', '2', '3']
machine = 15

for base in bases:
    print()
    print(f'ssh wangph1@circinus-{machine}.ics.uci.edu')

    for add in adds:
        spec = f'{base}{add}'
        print('run_blant_default.sh ~/plant/networks/snap/{spec}.el ~/plant/data/seeding_cached_data/blant_out/p0-o0-{spec}-lDEG2.out')

    machine += 1
