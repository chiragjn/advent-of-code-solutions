import sys
import time
from typing import Iterable, List


def diff(str1: str, str2: str) -> List[int]:
    if len(str1) == len(str2):
        return [i for i in range(len(str1)) if str1[i] != str2[i]]
    return []


def solve(input_iter: Iterable[str]) -> str:
    inp = [line.strip() for line in input_iter]
    for i in range(len(inp)):
        for j in range(i):
            positions = diff(inp[i], inp[j])
            if len(positions) == 1:
                return ''.join([c for k, c in enumerate(inp[i]) if k != positions[0]])

    return 'ERROR'


def run_tests():
    tests = [
        '''abcde
        fghij
        klmno
        pqrst
        fguij
        axcye
        wvxyz'''.split('\n'),
    ]

    answers = [
        'fgij'
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
