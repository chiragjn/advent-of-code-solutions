import collections
import sys
import time
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
