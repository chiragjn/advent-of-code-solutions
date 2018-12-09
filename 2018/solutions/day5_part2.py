import string
import sys
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
    return min(len(compress(polymer.replace(c.upper(), '').replace(c, ''))) for c in string.ascii_lowercase)


def run_tests():
    tests = [
        'dabAcCaCBAcCcaDA'
    ]

    answers = [
        4
    ]

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin.readline()))
