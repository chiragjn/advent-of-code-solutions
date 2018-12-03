import collections
import sys
from typing import Iterable


def solve(input_iter: Iterable[str]) -> int:
    twos, threes = 0, 0
    for line in input_iter:
        counts = collections.Counter(line.strip()).values()
        if 2 in counts:
            twos += 1
        if 3 in counts:
            threes += 1

    return twos * threes


def run_tests():
    tests = [
        ['abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab'],
    ]

    answers = [
        12
    ]

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
