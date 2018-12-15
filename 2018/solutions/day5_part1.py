import sys
import time
from typing import List


def compress(polymer: str) -> List[str]:
    stack: List[str] = []
    for c in polymer:
        if stack and stack[-1] != c and stack[-1].lower() == c.lower():
            stack.pop()
        else:
            stack.append(c)
    return stack


def solve(input_line: str) -> int:
    polymer = input_line.strip()
    compressed_polymer = compress(polymer)
    return len(compressed_polymer)


def run_tests():
    tests = [
        'aA',
        'abBA',
        'abAB',
        'aabAAB',
        'dabAcCaCBAcCcaDA'
    ]

    answers = [
        0,
        0,
        4,
        6,
        10,
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
    print(solve(sys.stdin.readline()))
