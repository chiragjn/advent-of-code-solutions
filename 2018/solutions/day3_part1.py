import re
import sys
import time
from typing import Iterable, List

FABRIC_SIZE = 1000
pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


def solve(input_iter: Iterable[str]) -> int:
    fabric: List[List[int]] = [[0 for __ in range(FABRIC_SIZE)] for _ in range(FABRIC_SIZE)]
    for line in input_iter:
        line = line.strip()
        match = pattern.search(line.strip())
        if not match:
            raise ValueError('Invalid input')
        claim_id, left_offset, top_offset, width, height = [int(x) for x in match.groups()]
        for i in range(left_offset, left_offset + width):
            for j in range(top_offset, top_offset + height):
                fabric[i][j] += 1

    answer = 0
    for i in range(FABRIC_SIZE):
        for j in range(FABRIC_SIZE):
            if fabric[i][j] > 1:
                answer += 1
    return answer


def run_tests():
    tests = [
        '''#1 @ 1,3: 4x4
        #2 @ 3,1: 4x4
        #3 @ 5,5: 2x2'''.split('\n')
    ]

    answers = [
        4
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
