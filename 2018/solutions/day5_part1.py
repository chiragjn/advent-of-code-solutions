import sys
from typing import List


def compress(polymer: str) -> List[str]:
    stack = []
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

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin.readline()))
