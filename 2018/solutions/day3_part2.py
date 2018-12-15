import re
import sys
import time
from typing import Iterable, Dict, List, Optional

FABRIC_SIZE = 1000
pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


class FabricSquare(object):
    def __init__(self, claim_count: int = 0, claimer: Optional[int] = None) -> None:
        self.claim_count = claim_count
        self.claimer = claimer


def solve(input_iter: Iterable[str]) -> int:
    claims: Dict[int, bool] = {}
    fabric: List[List[FabricSquare]] = [[FabricSquare() for __ in range(FABRIC_SIZE)] for _ in range(FABRIC_SIZE)]
    for line in input_iter:
        line = line.strip()
        match = pattern.search(line.strip())
        if not match:
            raise ValueError('Invalid input')
        claim_id, left_offset, top_offset, width, height = [int(x) for x in match.groups()]
        claims[claim_id] = True
        for i in range(left_offset, left_offset + width):
            for j in range(top_offset, top_offset + height):
                fabric[i][j].claim_count += 1
                if fabric[i][j].claimer is not None:
                    claims[fabric[i][j].claimer] = False  # type: ignore
                    claims[claim_id] = False
                fabric[i][j].claimer = claim_id

    for claim_id in claims:
        if claims[claim_id]:
            return claim_id

    return -1


def run_tests():
    tests = [
        '''#1 @ 1,3: 4x4
        #2 @ 3,1: 4x4
        #3 @ 5,5: 2x2'''.split('\n')
    ]

    answers = [
        3
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
