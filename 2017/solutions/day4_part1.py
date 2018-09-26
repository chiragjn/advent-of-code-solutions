import sys


def main():
    ans = 0
    for line in sys.stdin:
        ans += int(len(line.split()) == len(set(line.split())))
    print(ans)


if __name__ == '__main__':
    main()
