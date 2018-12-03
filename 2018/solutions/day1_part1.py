import sys
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

    for test, answer in zip(tests, answers):
        computed = solve(test)
        assert computed == answer, (test, answer, computed)


if __name__ == '__main__':
    run_tests()
    print(solve(sys.stdin))
