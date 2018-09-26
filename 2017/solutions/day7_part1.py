import sys


def main():
    parents = {}
    for line in sys.stdin:
        parts = line.strip().split('->')
        parent = parts[0].split()[0].strip()
        if parent not in parents:
            parents[parent] = parent

        if len(parts) > 1:
            children = list(map(str.strip, parts[1].split(', ')))
            for child in children:
                parents[child] = parent

    for k in parents:
        if parents[k] == k:
            print(k)


if __name__ == '__main__':
    main()
