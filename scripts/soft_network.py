import random
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def main():
    keep_ratio = float(sys.argv[1])
    f = open(sys.argv[2])
    lines = []

    for line in f:
        line = line.rstrip()

        if len(line.split(' ')) == 2:
            lines.append(line)
        else:
            eprint(f'line {line} is invalid')

    random.shuffle(lines)

    new_num_lines = int(keep_ratio * len(lines))

    for i in range(new_num_lines):
        print(lines[i])

if __name__ == '__main__':
    main()
