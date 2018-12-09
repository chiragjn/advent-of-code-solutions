import collections
import itertools
import sys
from typing import Iterable, List, NamedTuple, Set


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


def solve(input_iter: Iterable[str]) -> int:
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
            min_distance = min(distances)
            if distances.count(min_distance) == 1:
                grid[i][j] = coordinates[distances.index(min_distance)].name

    infinites: Set[int] = {0}
    for i in range(n):
        if grid[i][0]:
            infinites.add(grid[i][0])
        if grid[i][m - 1]:
            infinites.add(grid[i][m - 1])

    for i in range(m):
        if grid[0][i]:
            infinites.add(grid[0][i])
        if grid[n - 1][0]:
            infinites.add(grid[n - 1][0])

    for name, area in collections.Counter(itertools.chain.from_iterable(grid)).most_common():
        if name not in infinites:
            return area

    return -1


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
        17
    ]

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
