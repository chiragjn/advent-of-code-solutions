import sys
import time
from typing import Iterable, Any


def solve(input_iter: Iterable[str]) -> Any:
    for line in input_iter:
        line = line.strip()
        # do something

    return None


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