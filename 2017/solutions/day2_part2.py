import sys


def main():
    ans = 0
    for line in sys.stdin:
        l = sorted(map(int, line.strip().split()))
        for i, a in enumerate(l):
            for j, b in enumerate(l):
                if i != j and a % b == 0:
                    ans += (a // b)
    print(ans)

if __name__ == '__main__':
    main()
