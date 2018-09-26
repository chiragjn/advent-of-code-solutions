import sys


def main():
    l = [int(line.strip()) for line in sys.stdin]
    st = 0
    ans = 0
    while 0 <= st < len(l):
        c = st
        st += l[st]
        l[c] = (l[c] - 1) if l[c] >= 3 else (l[c] + 1)
        ans += 1
    print(ans)


if __name__ == '__main__':
    main()
