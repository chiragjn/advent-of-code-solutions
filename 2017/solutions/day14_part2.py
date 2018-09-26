from day10_part2 import solve

grid = []


def dfs(x, y):
    global grid
    if not ((0 <= x < len(grid)) and (0 <= y < len(grid[x])) and grid[x][y] == 1):
        return
    grid[x][y] = 0
    dfs(x - 1, y)
    dfs(x + 1, y)
    dfs(x, y - 1)
    dfs(x, y + 1)


def main():
    global grid
    inp = input().strip()
    ans = 0
    for i in range(128):
        hsh = solve('{0}-{1}'.format(inp, i))
        grid.append([])
        for c in hsh:
            cbinary = '{0:b}'.format(int(c, 16)).zfill(4)
            grid[-1].extend(list(map(int, cbinary)))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                ans += 1
                dfs(i, j)
    print(ans)


if __name__ == '__main__':
    main()
