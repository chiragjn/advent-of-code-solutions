import sys


def main():
    ans = 0
    for line in sys.stdin:
        words = [tuple(sorted(list(word))) for word in line.strip().split()]
        if len(words) == len(set(words)):
            ans += 1
    print(ans)


if __name__ == '__main__':
    main()
