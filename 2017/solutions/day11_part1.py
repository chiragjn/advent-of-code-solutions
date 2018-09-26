"""
The core idea to represent a hexagonal grid with three co-ordinates
was taken from this amazing article
https://www.redblobgames.com/grids/hexagons/#coordinates-cube
"""
ops = {
    'n': lambda x, y, z: (x, y + 1, z - 1),
    'nw': lambda x, y, z: (x - 1, y + 1, z),
    'ne': lambda x, y, z: (x + 1, y, z - 1),
    's': lambda x, y, z: (x, y - 1, z + 1),
    'sw': lambda x, y, z: (x - 1, y, z + 1),
    'se': lambda x, y, z: (x + 1, y - 1, z),
}


def dist(A, B):
    return max(
        abs(A[0] - B[0]),
        abs(A[1] - B[1]),
        abs(A[2] - B[2]),
    )


def main():
    start = (0, 0, 0)
    end = (0, 0, 0)
    moves = input().strip().split(',')
    for move in moves:
        end = ops[move](*end)
    print(dist(start, end))


if __name__ == '__main__':
    main()
