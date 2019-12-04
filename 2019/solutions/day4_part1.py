import sys
import time
import itertools
from typing import Iterable


def is_valid(sequence: int) -> bool:
    sequence = list(str(sequence))
    increasing = sequence == list(sorted(sequence))
    repeating = any(len(list(group)) > 1 for _, group in itertools.groupby(sequence))
    return increasing and repeating


def solve(input_iter: Iterable[str]) -> int:
    line = next(iter(input_iter))
    low, high = [int(x) for x in line.strip().split('-')]
    counter = 0
    for i in range(low, high + 1):
        if is_valid(i):
            counter += 1

    return counter


def run_tests():
    tests = [

    ]

    answers = [

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
