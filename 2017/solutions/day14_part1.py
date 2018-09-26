from day10_part2 import solve


def main():
    inp = input().strip()
    ans = 0
    for i in range(128):
        hsh = solve('{0}-{1}'.format(inp, i))
        bin_hsh = ''.join(['{0:b}'.format(int(c, 16)).zfill(4)
                           for c in hsh])
        ans += bin_hsh.count('1')
    print(ans)


if __name__ == '__main__':
    main()
