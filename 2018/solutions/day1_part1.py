import sys
import time
from typing import Dict, Iterable, Callable


def add(a: int, b: int) -> int:
    return a + b


def sub(a: int, b: int) -> int:
    return a - b


ops: Dict[str, Callable[[int, int], int]] = {'+': add, '-': sub}


def solve(input_iter: Iterable[str]) -> int:
    ans = 0
    for line in input_iter:
        line = line.strip()
        operator, operand = ops[line[:1]], int(line[1:])
        ans = operator(ans, operand)
    return ans


def run_tests():
    tests = [
        "+1, -1".split(', '),
        "+3, +3, +4, -2, -4".split(', '),
        "-6, +3, +8, +5, -6".split(', '),
        "+7, +7, -2, -7, -4".split(', '),
    ]

    answers = [
        0,
        4,
        4,
        1
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
