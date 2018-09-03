import sys


def main():
    ans = 0
    for line in sys.stdin:
        l = sorted(map(int, line.strip().split()))
        ans += l[-1] - l[0]
    print(ans)

if __name__ == '__main__':
    main()
