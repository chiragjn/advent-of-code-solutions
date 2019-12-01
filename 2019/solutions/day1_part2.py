import sys
import time
from typing import Iterable


def compute_fuel(x: int) -> int:
    y = max(0, ((x // 3) - 2))
    return y + compute_fuel(y) if y > 0 else y


def solve(input_iter: Iterable[str]) -> int:
    modules = [int(line.strip()) for line in input_iter]
    return sum(compute_fuel(module) for module in modules)


def run_tests():
    tests = [
        ["12"],
        ["14"],
        ["1969"],
        ["100756"],
    ]

    answers = [
        2,
        2,
        966,
        50346,
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
