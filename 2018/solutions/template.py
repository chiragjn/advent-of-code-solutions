import sys
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

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
