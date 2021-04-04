import sys
import os

def main():
    global k
    k = int(sys.argv[1])
    path = sys.argv[2]

    if not os.path.exists(path):
        print(f'{path} does not exist')
        return

    if os.path.isdir(path):
        dir_get_nc(path)
    elif os.path.isfile(path):
        file_get_nc(path)
    else:
        print(f'the path {path} is neither a file nor a directory')

def dir_get_nc(dirpath):
    print(f'dir_get_nc called for {dirpath}')

    for entry in os.scandir(dirpath):
        if os.path.isdir(entry.path):
            dir_get_nc(entry.path)
        elif os.path.isfile(entry.path):
            file_get_nc(entry.path)
        else:
            print(f'the path {path} is neither a file nor a directory')

def file_get_nc(filepath):
    print(f'file_get_nc called for {filepath}')

    f = open(filepath, 'r')
    found_nodes = set()
    
    for line in f:
        line = line.rstrip()
        nodes = line.split(' ')

        if len(nodes) != k + 1:
            print(f'the line "{line}" in {filepath} is not the correct format')
        else:
            for i, node in enumerate(nodes):
                if i != 0:
                    found_nodes.add(node)

    print(f'{filepath} {len(found_nodes)}')


if __name__ == '__main__':
    main()

