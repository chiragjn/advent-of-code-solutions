import collections
import sys
import time
from typing import Iterable, Iterator, Tuple, Dict, Callable


def move_right(x: int, y: int, steps: int) -> Iterator[Tuple[int, int]]:
    for i in range(1, steps + 1):
        yield x + i, y


def move_left(x: int, y: int, steps: int) -> Iterator[Tuple[int, int]]:
    for i in range(1, steps + 1):
        yield x - i, y


def move_up(x: int, y: int, steps: int) -> Iterator[Tuple[int, int]]:
    for i in range(1, steps + 1):
        yield x, y + i


def move_down(x: int, y: int, steps: int) -> Iterator[Tuple[int, int]]:
    for i in range(1, steps + 1):
        yield x, y - i


def solve(input_iter: Iterable[str]) -> int:
    move_registry: Dict[str, Callable[[int, int, int], Iterator[Tuple[int, int]]]] = {
        'R': move_right,
        'L': move_left,
        'U': move_up,
        'D': move_down,
    }
    start_x, start_y = 0, 0
    grid: Dict[Tuple[int, int], int] = collections.defaultdict(int)
    for wire_no, line in enumerate(input_iter):
        moves = line.strip().split(',')
        x, y = start_x, start_y
        for move in moves:
            direction, steps = move[0], move[1:]
            steps = int(steps)
            for i, j in move_registry[direction](x, y, steps):
                grid[(i, j)] |= (1 << wire_no)
                x, y = i, j

    answer = int(1e9)
    for (kx, ky), wire_mask in grid.items():
        if wire_mask == 3:
            answer = min(answer, abs(kx - start_x) + abs(ky - start_y))

    return answer


def run_tests():
    tests = [
        ["R8,U5,L5,D3", "U7,R6,D4,L4"],
        ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"],
        ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"],
    ]

    answers = [
        6,
        159,
        135,
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
