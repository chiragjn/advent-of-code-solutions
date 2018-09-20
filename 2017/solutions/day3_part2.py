import collections

def get_xy(number):
    if number == 1:
        return 0, 0
    k = 0
    x, y = 0, 0
    z = 1
    while z < number:
        k += 2
        z = (k + 1) * (k + 1)
        x += 1
        y -= 1
    
    ops = [lambda x, y: (x - 1, y),
           lambda x, y: (x, y + 1),
           lambda x, y: (x + 1, y),
           lambda x, y: (x, y - 1)]
    
    if z == number:
        return x, y

    for i in range(4):
        op = ops[i]
        for _ in range(k):
            z -= 1
            x, y = op(x, y)
            if z == number:
                return x, y
    
    return None, None

def get_neighbors(x, y):
    return [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
            (x, y - 1), (x, y + 1),
            (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

grid = collections.defaultdict(int)

def main():
    n = int(input())
    grid[(0, 0)] = 1
    z = grid[(0, 0)]
    i = 2
    while z < n:
        coords = get_xy(i)
        grid[coords] = sum(grid[c] for c in get_neighbors(*coords))
        z = grid[coords]
        i += 1

    print(z)

if __name__ == '__main__':
    main()
