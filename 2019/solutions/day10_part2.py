import math
import operator
import sys
import time
from typing import Iterable, Tuple, Dict, List


def reduce_fraction(numerator: int, denominator: int) -> Tuple[int, int]:
    g = math.gcd(numerator, denominator)
    return numerator // g, denominator // g


def l2_norm(x1: int, y1: int, x2: int, y2: int) -> float:
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


def visible_asteroids(grid: List[str], x: int, y: int) -> int:
    memory: Dict[Tuple[int, int], Tuple[int, int]] = {}
    for i, row in enumerate(grid, start=1):
        for j, c in enumerate(row, start=1):
            if (i == x and j == y) or c == '.':
                continue
            key = reduce_fraction(j - y, i - x)
            if (key not in memory
                    or (l2_norm(i, j, x, y) < l2_norm(memory[key][0], memory[key][1], x, y))):
                memory[key] = (i, j)
    return len(memory)


def best_asteroid(grid: List[str]) -> Tuple[int, int]:
    asteroid_counts: List[Tuple[Tuple[int, int], int]] = []
    for i, row in enumerate(grid, start=1):
        for j, c in enumerate(row, start=1):
            if c == '#':
                asteroid_counts.append(((i, j), visible_asteroids(grid, i, j)))
    return max(asteroid_counts, key=operator.itemgetter(1))[0]


def spiral_sort(ox: int, oy: int, coordinates: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    pass


def solve(input_iter: Iterable[str]) -> int:
    grid = []
    for line in input_iter:
        line = line.strip()
        grid.append(line)
    x, y = best_asteroid(grid)
    coordinates = [(i, j) for i, row in enumerate(grid, start=1) for j, c in enumerate(row, start=1)
                   if c == '#' and (i, j) != (x, y)]
    coordinates = spiral_sort(ox=x, oy=y, coordinates=coordinates)
    x, y = coordinates[200]
    return x * 100 + y


def run_tests():
    tests = [
        """.#..#
        .....
        #####
        ....#
        ...##""".split('\n'),

        """......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####""".split('\n'),

        """#.#...#.#.
        .###....#.
        .#....#...
        ##.#.#.#.#
        ....#.#.#.
        .##..###.#
        ..#...##..
        ..##....##
        ......#...
        .####.###.""".split('\n'),

        """.#..#..###
        ####.###.#
        ....###.#.
        ..###.##.#
        ##.##.#.#.
        ....###..#
        ..#.#..#.#
        #..#.#.###
        .##...##.#
        .....#.#..""".split('\n'),

        """.#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##""".split('\n'),
    ]

    answers = [
        8,
        33,
        35,
        41,
        210
    ]

    for i, (test, answer) in enumerate(zip(tests, answers), start=1):
        print('Running test: {}/{}'.format(i, len(tests)))
        start = time.time()
        computed = solve(test)
        end = time.time()
        assert computed == answer, (test, answer, computed)
        print('OK. Took {:.2f}'.format(end - start))


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
