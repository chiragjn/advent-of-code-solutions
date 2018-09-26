import sys


def main():
    ans = 0
    for line in sys.stdin:
        layer, depth = list(map(int, line.strip().split(': ')))
        if layer % (2 * depth - 2) == 0:
            ans += (layer * depth)
    print(ans)


if __name__ == '__main__':
    main()
