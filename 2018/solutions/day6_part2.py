import collections
import itertools
import sys
import time
from typing import Iterable, List, NamedTuple


class Coordinate(NamedTuple):
    name: int
    x: int
    y: int

    def distance(self, i: int, j: int) -> int:
        return abs(self.x - i) + abs(self.y - j)

    def __str__(self) -> str:
        return 'name: {}, x: {}, y: {}'.format(self.name, self.x, self.y)

    def __repr__(self) -> str:
        return str(self)


def solve(input_iter: Iterable[str], max_dist: int = 10000) -> int:
    coordinates: List[Coordinate] = []
    x_max, y_max = 0, 0
    for i, line in enumerate(input_iter, start=1):
        y, x = [int(coord) for coord in line.strip().split(', ')]
        # the above order of y, x is not a bug.
        coordinates.append(Coordinate(name=i, x=x, y=y))
        x_max = max(x_max, x)
        y_max = max(y_max, y)

    n = x_max + 1
    m = y_max + 1
    grid: List[List[int]] = [[0 for __ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            distances = [coordinate.distance(i, j) for coordinate in coordinates]
            all_distances = sum(distances)
            if all_distances < max_dist:
                grid[i][j] = 1

    sizes = collections.Counter(itertools.chain.from_iterable(grid))
    return sizes.get(1, 0)


def run_tests():
    tests = [
        '''1, 1
        1, 6
        8, 3
        3, 4
        5, 5
        8, 9'''.split('\n')
    ]

    answers = [
        16
    ]

    for i, (test, answer) in enumerate(zip(tests, answers), start=1):
        print('Running test: {}/{}'.format(i, len(tests)))
        start = time.time()
        computed = solve(test, max_dist=32)
        end = time.time()
        assert computed == answer, (test, answer, computed)
        print('OK. Took {:.2f}'.format(end - start))


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
